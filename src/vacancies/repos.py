from uuid import UUID
import typing as tp

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.future import select
from sqlalchemy import delete, update
from sqlalchemy import exc as sa_exc

from ..skills.repos import SkillsRepo
from ..service import models as m
from ..service.pd_models import (
    vacancy,
    vacancy_skill,
    skill
)


class VacanciesRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def get_one(self, id: UUID, company_id: UUID) -> vacancy.Read:
        stmt = select(m.Vacancy) \
               .join(m.Vacancy.creator) \
               .where(m.Vacancy.id == id) \
               .where(m.User.company_id == company_id) \
               .where(m.Vacancy.is_deleted == False)
               
        try:
            vacancy_orm = (await self._session.scalars(stmt)).one()
        except sa_exc.NoResultFound:
            raise #  TODO: custom exceptions
        
        return vacancy.Read.from_orm(vacancy_orm)
        
    async def get_list(self, company_id: UUID, filters: vacancy.Filters) -> tp.List[vacancy.Read]:
        stmt = select(m.Vacancy) \
               .join(m.Vacancy.creator) \
               .where(m.User.company_id == company_id) \
               .where(m.Vacancy.is_deleted == False) \
               .order_by(m.Vacancy.created_at.desc())
        
        if filters.recruiter_id is not None:
            stmt = stmt.filter(m.Vacancy.recruiter_id == filters.recruiter_id)
        if filters.department_id is not None:
            stmt = stmt.filter(m.Vacancy.department_id == filters.department_id)
        if filters.position_id is not None:
            stmt = stmt.filter(m.Vacancy.position_id == filters.position_id)
        if filters.grade_id is not None:
            stmt = stmt.filter(m.Vacancy.grade_id == filters.grade_id)
        if filters.priority_code is not None:
            stmt = stmt.filter(m.Vacancy.priority_code == filters.priority_code)
        if filters.adress_code is not None:
            stmt = stmt.filter(m.Vacancy.adress_code == filters.adress_code)
        if filters.status_code is not None:
            stmt = stmt.filter(m.Vacancy.status_code == filters.status_code)
        if filters.date_from is not None:
            stmt = stmt.filter(m.Vacancy.created_at >= filters.date_from)
        if filters.date_to is not None:
            stmt = stmt.filter(m.Vacancy.created_at <= filters.date_to)
            
        if filters.salary_from is not None:
            stmt = stmt.filter((coalesce(m.Vacancy.salary_to, m.Vacancy.salary_from) >= filters.salary_from))
        if filters.salary_to is not None:
            stmt = stmt.filter((coalesce(m.Vacancy.salary_from, m.Vacancy.salary_to) <= filters.salary_to))
        
        # if filters.skills is not None:
        #     stmt = stmt.filter(m.Vacancy)
        
        res = await self._session.scalars(stmt)
        return [vacancy.Read.from_orm(vacancy_orm) for vacancy_orm in res.all()]
    
    async def delete(self, id: UUID, company_id: UUID) -> UUID:
        # TODO: check company id
        stmt = update(m.Vacancy) \
               .where(m.Vacancy.id == id) \
               .where(m.Vacancy.is_deleted == False) \
               .values(is_deleted=True) \
               .returning(m.Vacancy.id)
               
        try:
            vacancy_id = (await self._session.scalars(stmt)).one()
        except sa_exc.NoResultFound:
            raise #  TODO: custom exceptions
        
        return vacancy_id

    async def add(self, initiator_id: UUID, pd_model: vacancy.Create) -> UUID:
        stmt = select(m.User.company_id).where(m.User.id == initiator_id)
        res = await self._session.execute(stmt)
        company_id = res.scalars().one()
        
        vacancy_data = pd_model.dict_vacancy_only()
        vacancy_data['creator_id'] = initiator_id
        vacancy_data['company_id'] = company_id
        vacancy_data['status_code'] = 1
        
        stmt = insert(m.Vacancy).values(vacancy_data).returning(m.Vacancy.id)
        res = await self._session.execute(stmt)
        vacancy_id = res.scalars().one()
        
        skills_repo = SkillsRepo(self._session)
        
        new_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, skill.Create)]
        existing_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, vacancy_skill.Create)]
        
        new_skill_ids = await skills_repo.add_many(company_id, new_skills)
        
        existing_skills.extend([vacancy_skill.Create(skill_id=new_skill_id) for new_skill_id in new_skill_ids])
        
        await self._add_child_entities(initiator_id, vacancy_id, existing_skills, m.VacancySkill)
        return vacancy_id
        
    async def _add_child_entities(self, initiator_id: UUID, vacancy_id: UUID, entities_list, sa_model: DeclarativeMeta):
        prepared_entities = []
        for entity in entities_list:
            entity_dict = entity.dict()
            entity_dict['creator_id'] = initiator_id
            entity_dict['vacancy_id'] = vacancy_id
            prepared_entities.append(entity_dict)
            
        stmt = insert(sa_model).values(prepared_entities).returning(sa_model.id)
        res = await self._session.execute(stmt)  
        entities_ids = res.scalars().all()
        return entities_ids
    
    async def update(self, vacancy_id: UUID, initiator_id: UUID,  pd_model: vacancy.Update) -> UUID:
        stmt = select(m.User.company_id).where(m.User.id == initiator_id)
        res = await self._session.execute(stmt)
        company_id = res.scalars().one()
        
        vacancy_data = pd_model.dict_vacancy_only()
        vacancy_data['creator_id'] = initiator_id
        vacancy_data['company_id'] = company_id
        
        stmt = update(m.Vacancy) \
               .values(vacancy_data) \
               .where(m.Vacancy.id == vacancy_id) \
               .where(m.Vacancy.is_deleted == False) \
               .returning(m.Vacancy.id)
        
        try:
            (await self._session.scalars(stmt)).one()
        except (sa_exc.NoResultFound, sa_exc.IntegrityError):
            raise #  TODO: custom exceptions
        
        skills_repo = SkillsRepo(self._session)
        
        new_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, skill.Create)]
        existing_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, vacancy_skill.Update)]
        
        new_skill_ids = await skills_repo.add_many(company_id, new_skills)
        
        existing_skills.extend([vacancy_skill.Update(skill_id=new_skill_id) for new_skill_id in new_skill_ids])
        
        await self._update_child_entities(initiator_id, vacancy_id, existing_skills, m.VacancySkill)
        return vacancy_id
        
    async def _update_child_entities(self, initiator_id: UUID, vacancy_id: UUID, entities_list, sa_model: DeclarativeMeta):
        entities_ids = [entity.id for entity in entities_list if entity.id is not None]
        stmt = delete(sa_model) \
              .where(sa_model.id.not_in(entities_ids)) \
              .where(sa_model.vacancy_id == vacancy_id)
        
        await self._session.execute(stmt)
        
        if not entities_list:
            return 
        
        for entity in entities_list:
            entity_dict = entity.dict(exclude_none=True)
            entity_dict['creator_id'] = initiator_id
            entity_dict['vacancy_id'] = vacancy_id
            stmt = insert(sa_model) \
                   .values(**entity_dict) \
                   .on_conflict_do_update(index_elements=[sa_model.id],
                                          where=(sa_model.vacancy_id == vacancy_id),
                                          set_=entity_dict)
            await self._session.execute(stmt)
