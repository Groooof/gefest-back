from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete, update
from sqlalchemy.orm.decl_api import DeclarativeMeta

from ..service import models as m
from ..service.pd_models import candidate
from ..service.pd_models import skill
from ..service.pd_models import candidate_skill
from ..skills.repos import SkillsRepo


class CandidatesRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def add(self, creator_id: UUID, pd_model: candidate.Create) -> UUID:
        stmt = select(m.User.company_id).where(m.User.id == creator_id)
        res = await self._session.execute(stmt)
        company_id = res.scalars().one()
        
        candidate_data = pd_model.dict_candidate_only()
        candidate_data['creator_id'] = creator_id
        
        stmt = insert(m.Candidate).values(candidate_data).returning(m.Candidate.id)
        res = await self._session.execute(stmt)
        candidate_id = res.scalars().one()
        
        skills_repo = SkillsRepo(self._session)
        
        new_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, skill.Create)]
        existing_skills = [_skill for _skill in pd_model.skills if isinstance(_skill, candidate_skill.Create)]
        
        new_skill_ids = await skills_repo.add_many(company_id, new_skills)
        
        existing_skills.extend([candidate_skill.Create(skill_id=new_skill_id) for new_skill_id in new_skill_ids])
        
        await self._add_child_entities(creator_id, candidate_id, existing_skills, m.CandidateSkill)
        await self._add_child_entities(creator_id, candidate_id, pd_model.contacts, m.CandidateContact)
        await self._add_child_entities(creator_id, candidate_id, pd_model.work_places, m.CandidateWorkPlace)
        await self._add_child_entities(creator_id, candidate_id, pd_model.languages, m.CandidateLanguageAbility)
        await self._add_child_entities(creator_id, candidate_id, pd_model.notes, m.CandidateNote)
        return candidate_id
        
    async def _add_child_entities(self, creator_id: UUID, candidate_id: UUID, entities_list, sa_model: DeclarativeMeta):
        prepared_entities = []
        for entity in entities_list:
            entity_dict = entity.dict()
            entity_dict['creator_id'] = creator_id
            entity_dict['candidate_id'] = candidate_id
            prepared_entities.append(entity_dict)
            
        stmt = insert(sa_model).values(prepared_entities).returning(sa_model.id)
        res = await self._session.execute(stmt)  
        entities_ids = res.scalars().all()
        return entities_ids