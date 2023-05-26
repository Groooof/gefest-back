from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete, update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import exc as sa_exc
from sqlalchemy.ext.asyncio import AsyncSession

from ..service import models as m

from ..service.roles import Roles
from ..service.dependencies import (
    AccessJWTCookie,
    CheckRoles,
    get_session
)

from . import schemas as sch
from ..service.tokens import (
    AccessToken,
)

from ..service import exceptions as exc
from ..service.fastapi_custom import generate_openapi_responses


router = APIRouter(tags=['candidates'], prefix='/candidates')


@router.post('',
             name='Создание карточки кандидата',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.Create.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
             )
async def create(body: sch.Create.Request.Body,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Добавляет кандидата в систему
    '''
    
    stmt = select(m.User.company_id).where(m.User.id == at.user_id)
    res = await session.execute(stmt)
    company_id = res.scalars().one()
    
    stmt = insert(m.Candidate).values(creator_id=at.user_id, **body.candidate.dict()).returning(m.Candidate.id)
    res = await session.execute(stmt)
    await session.commit()
    
    candidate_id = res.scalars().one()
    
    contacts_for_insert = []
    for contact in body.contacts:
        contact_dict = contact.dict()
        contact_dict['creator_id'] = at.user_id
        contact_dict['candidate_id'] = candidate_id
        contacts_for_insert.append(contact_dict)
        
    stmt = insert(m.CandidateContact).values(contacts_for_insert)
    res = await session.execute(stmt)    
    await session.commit()
    
    work_expirience_for_insert = []
    for expirience in body.expiriense:
        expirience_dict = expirience.dict()
        expirience_dict['creator_id'] = at.user_id
        expirience_dict['candidate_id'] = candidate_id
        work_expirience_for_insert.append(expirience_dict)
        
    stmt = insert(m.CandidateWorkExpirience).values(work_expirience_for_insert)
    res = await session.execute(stmt)    
    await session.commit()
    
    languages_for_insert = []
    for lang in body.languages:
        lang_dict = lang.dict()
        lang_dict['creator_id'] = at.user_id
        lang_dict['candidate_id'] = candidate_id
        languages_for_insert.append(lang_dict)
        
    stmt = insert(m.CandidateLanguageAbility).values(languages_for_insert)
    res = await session.execute(stmt)    
    await session.commit()
    
    notes_for_insert = []
    for note in body.notes:
        note_dict = {}
        note_dict['note'] = note
        note_dict['creator_id'] = at.user_id
        note_dict['candidate_id'] = candidate_id
        notes_for_insert.append(note_dict)
        
    stmt = insert(m.CandidateNote).values(notes_for_insert)
    res = await session.execute(stmt)    
    await session.commit()
    
    new_skills_for_insert = []
    existing_skills_for_insert = []
    for skill in body.skills:
        if isinstance(skill, sch.NewSkill):
            new_skill_dict = skill.dict()
            new_skill_dict['normalized_name'] = skill.name.capitalize()
            new_skill_dict['company_id'] = company_id
            new_skills_for_insert.append(new_skill_dict)
        else:
            existing_skill_dict = skill.dict()
            existing_skill_dict['creator_id'] = at.user_id
            existing_skill_dict['candidate_id'] = candidate_id
            existing_skills_for_insert.append(existing_skill_dict)
            
    stmt = insert(m.Skill).values(new_skills_for_insert).returning(m.Skill.id)
    res = await session.execute(stmt)   
    await session.commit() 
    
    new_skill_ids = res.scalars().all()
    for skill_id in new_skill_ids:
        existing_skill_dict = {}
        existing_skill_dict['skill_id'] = skill_id
        existing_skill_dict['creator_id'] = at.user_id
        existing_skill_dict['candidate_id'] = candidate_id
        existing_skills_for_insert.append(existing_skill_dict)
    
    stmt = insert(m.CandidateSkill).values(existing_skills_for_insert)
    res = await session.execute(stmt)
    await session.commit()

    return sch.Create.Response.Body(id=candidate_id)
