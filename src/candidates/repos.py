from uuid import UUID
import typing as tp

from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from sqlalchemy import delete, update
from sqlalchemy import exc as sa_exc

from ..skills.repos import SkillsRepo
from ..service import models as m
from ..service.pd_models import (
    candidate,
    skill,
    candidate_skill
)


class CandidatesRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def get_one(self, id: UUID, company_id: UUID) -> candidate.Read:
        stmt = select(m.Candidate) \
               .join(m.Candidate.creator) \
               .where(m.Candidate.id == id) \
               .where(m.User.company_id == company_id) \
               .where(m.Candidate.is_deleted == False)
                
        res = await self._session.scalars(stmt)
        try:
            candidate_orm = res.one()
        except sa_exc.NoResultFound:
            raise #  TODO: custom exceptions
        
        return candidate.Read.from_orm(candidate_orm)
        
    async def get_list(self, company_id: UUID, filters: candidate.Filters) -> tp.List[candidate.Read]:
        
        stmt = select(m.Candidate) \
               .join(m.Candidate.creator) \
               .where(m.User.company_id == company_id) \
               .where(m.Candidate.is_deleted == False) \
               .order_by(m.Candidate.created_at.desc())
        
        if filters.first_name is not None:
            stmt = stmt.filter(m.Candidate.first_name.ilike(f'%{filters.first_name}%'))
        if filters.last_name is not None:
            stmt = stmt.filter(m.Candidate.last_name.ilike(f'%{filters.last_name}%'))
        if filters.middle_name is not None:
            stmt = stmt.filter(m.Candidate.middle_name.ilike(f'%{filters.middle_name}%'))
        if filters.date_from is not None:
            stmt = stmt.filter(m.Candidate.created_at >= filters.date_from)
        if filters.date_to is not None:
            stmt = stmt.filter(m.Candidate.created_at <= filters.date_to)
        if filters.position_id is not None:
            stmt = stmt.filter(m.Candidate.position_id == filters.position_id)
        if filters.salary_from is not None:
            stmt = stmt.filter(m.Candidate.min_salary >= filters.salary_from)
        if filters.salary_to is not None:
            stmt = stmt.filter(m.Candidate.min_salary <= filters.salary_to)
        
        res = await self._session.scalars(stmt)
        candidates_orm = res.all()
        return [candidate.Read.from_orm(candidate_orm) for candidate_orm in candidates_orm]
    
    async def delete(self, id: UUID, company_id: UUID) -> UUID:
        # TODO: check company id
        stmt = update(m.Candidate) \
               .where(m.Candidate.id == id) \
               .where(m.Candidate.is_deleted == False) \
               .values(is_deleted=True) \
               .returning(m.Candidate.id)
               
        res = await self._session.scalars(stmt)
        try:
            candidate_id = res.one()
        except sa_exc.NoResultFound:
            raise #  TODO: custom exceptions
        
        return candidate_id
    
    async def add(self, initiator_id: UUID, pd_model: candidate.Create) -> UUID:
        stmt = select(m.User.company_id).where(m.User.id == initiator_id)
        res = await self._session.execute(stmt)
        company_id = res.scalars().one()
        
        # добавляем данные в таблицу кандидата
        candidate_data = pd_model.dict_candidate_only()
        candidate_data['creator_id'] = initiator_id
        
        stmt = insert(m.Candidate).values(candidate_data).returning(m.Candidate.id)
        res = await self._session.execute(stmt)
        candidate_id = res.scalars().one()
        
        skills_repo = SkillsRepo(self._session)
        
        # разделяем полученный список навыков на уже существующие и новые (которые нужно добавить)
        new_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, skill.Create)]
        existing_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, candidate_skill.Create)]
        
        # добавляем новые и получаем их id
        new_skill_ids = await skills_repo.add_many(company_id, new_skills)
        
        # добавляем вставленные навыки в список уже существующих
        existing_skills.extend([candidate_skill.Create(skill_id=new_skill_id) for new_skill_id in new_skill_ids])
        
        # добавляем дочерние сущности кандидата в соответствующие таблицы
        await self._add_child_entities(initiator_id, candidate_id, existing_skills, m.CandidateSkill)
        await self._add_child_entities(initiator_id, candidate_id, pd_model.contacts, m.CandidateContact)
        await self._add_child_entities(initiator_id, candidate_id, pd_model.work_places, m.CandidateWorkPlace)
        await self._add_child_entities(initiator_id, candidate_id, pd_model.languages, m.CandidateLanguageAbility)
        await self._add_child_entities(initiator_id, candidate_id, pd_model.notes, m.CandidateNote)
        return candidate_id
        
    async def _add_child_entities(self, initiator_id: UUID, candidate_id: UUID, entities_list, sa_model: DeclarativeMeta):
        prepared_entities = []
        for entity in entities_list:
            entity_dict = entity.dict()
            entity_dict['creator_id'] = initiator_id
            entity_dict['candidate_id'] = candidate_id
            prepared_entities.append(entity_dict)
            
        stmt = insert(sa_model).values(prepared_entities).returning(sa_model.id)
        res = await self._session.execute(stmt)  
        entities_ids = res.scalars().all()
        return entities_ids
    
    async def update(self, candidate_id: UUID, initiator_id: UUID,  pd_model: candidate.Update):
        # выполяем действия, аналогичные тем, что в методе add
        # обновляем данные самого кандидата, парсим навыки и обновляем все
        # дочерние сущености
        stmt = select(m.User.company_id).where(m.User.id == initiator_id)
        res = await self._session.execute(stmt)
        company_id = res.scalars().one()
        
        candidate_data = pd_model.dict_candidate_only()
        candidate_data['creator_id'] = initiator_id
        
        stmt = update(m.Candidate) \
               .values(candidate_data) \
               .where(m.Candidate.id == candidate_id) \
               .where(m.Candidate.is_deleted == False) \
               .returning(m.Candidate.id) 

        res = await self._session.execute(stmt)
        try:
            _ = res.scalars().one()
        except (sa_exc.NoResultFound, sa_exc.IntegrityError):
            raise #  TODO: custom exceptions
        
        skills_repo = SkillsRepo(self._session)
        
        new_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, skill.Create)]
        existing_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, candidate_skill.Update)]
        
        new_skill_ids = await skills_repo.add_many(company_id, new_skills)
        
        existing_skills.extend([candidate_skill.Update(skill_id=new_skill_id) for new_skill_id in new_skill_ids])
        
        await self._update_child_entities(initiator_id, candidate_id, existing_skills, m.CandidateSkill)
        await self._update_child_entities(initiator_id, candidate_id, pd_model.contacts, m.CandidateContact)
        await self._update_child_entities(initiator_id, candidate_id, pd_model.work_places, m.CandidateWorkPlace)
        await self._update_child_entities(initiator_id, candidate_id, pd_model.languages, m.CandidateLanguageAbility)
        await self._update_child_entities(initiator_id, candidate_id, pd_model.notes, m.CandidateNote)
        return candidate_id
        
    async def _update_child_entities(self, initiator_id: UUID, candidate_id: UUID, entities_list, sa_model: DeclarativeMeta):
        # удаляем все записи, которых нет в списке полученных
        entities_ids = [entity.id for entity in entities_list if entity.id is not None]
        stmt = delete(sa_model) \
               .where(sa_model.id.not_in(entities_ids)) \
               .where(sa_model.candidate_id == candidate_id)
               
        await self._session.execute(stmt)
        
        if not entities_list:
            return 
        
        # вставляем новые записи и обновляем страые
        for entity in entities_list:
            entity_dict = entity.dict(exclude_none=True)
            entity_dict['creator_id'] = initiator_id
            entity_dict['candidate_id'] = candidate_id
            stmt = insert(sa_model) \
                   .values(**entity_dict) \
                   .on_conflict_do_update(index_elements=[sa_model.id],
                                          where=(sa_model.candidate_id == candidate_id),
                                          set_=entity_dict)
            await self._session.execute(stmt)
