from uuid import UUID
import typing as tp

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..service import models as m
from ..service.pd_models import skill


class SkillsRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_many(self, company_id: UUID, pd_models_list: tp.List[skill.Create]) -> tp.List[UUID]:
        if not pd_models_list:
            return []
        
        skills_for_insert = []
        for skill in pd_models_list:
            skill_dict = skill.dict()
            skill_dict['normalized_name'] = skill.name.capitalize()
            skill_dict['company_id'] = company_id
            skills_for_insert.append(skill_dict)
            
        stmt = insert(m.Skill).values(skills_for_insert)
        stmt = stmt \
               .on_conflict_do_update(index_elements=[m.Skill.normalized_name],
                                      set_=dict(normalized_name=stmt.excluded.normalized_name)) \
               .returning(m.Skill.id)
        
        stmt = select(m.Skill.id).from_statement(stmt).execution_options(populate_existing=True)
        res = await self._session.execute(stmt)   
        skill_ids = res.scalars().all()
        return skill_ids
