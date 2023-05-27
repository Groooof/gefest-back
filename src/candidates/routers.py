from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    Query
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
                 exc.InvalidClientError,
                 exc.AccessDenied
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
    
    candidate_data = body.dict_candidate_only()
    candidate_data['creator_id'] = at.user_id
    
    stmt = insert(m.Candidate).values(candidate_data).returning(m.Candidate.id)
    res = await session.execute(stmt)
    
    candidate_id = res.scalars().one()
    
    contacts_for_insert = []
    for contact in body.contacts:
        contact_dict = contact.dict()
        contact_dict['creator_id'] = at.user_id
        contact_dict['candidate_id'] = candidate_id
        contacts_for_insert.append(contact_dict)
        
    stmt = insert(m.CandidateContact).values(contacts_for_insert)
    res = await session.execute(stmt)    
    
    work_places_for_insert = []
    for work_place in body.work_places:
        work_place_dict = work_place.dict()
        work_place_dict['creator_id'] = at.user_id
        work_place_dict['candidate_id'] = candidate_id
        work_places_for_insert.append(work_place_dict)
        
    stmt = insert(m.CandidateWorkPlace).values(work_places_for_insert)
    res = await session.execute(stmt)    
    
    languages_for_insert = []
    for lang in body.languages:
        lang_dict = lang.dict()
        lang_dict['creator_id'] = at.user_id
        lang_dict['candidate_id'] = candidate_id
        languages_for_insert.append(lang_dict)
        
    stmt = insert(m.CandidateLanguageAbility).values(languages_for_insert)
    res = await session.execute(stmt)    
    
    notes_for_insert = []
    for note in body.notes:
        note_dict = note.dict()
        note_dict['creator_id'] = at.user_id
        note_dict['candidate_id'] = candidate_id
        notes_for_insert.append(note_dict)
        
    stmt = insert(m.CandidateNote).values(notes_for_insert)
    res = await session.execute(stmt)    
    
    new_skills_for_insert = []
    existing_skills_for_insert = []
    for skill in body.skills:
        if isinstance(skill, sch.candidate.skill.Create):
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


@router.patch('/{id}',
             name='Обновление данных кандидата',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied
                 ),
            #  response_model=sch.Update.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
             )
async def update_candidate(id: UUID,
                           body: sch.Update.Request.Body,
                           session: AsyncSession = Depends(get_session),
                           at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Обновление данных кандидата
    '''

    candidate_id = id

    stmt = select(m.User.company_id).where(m.User.id == at.user_id)
    res = await session.execute(stmt)
    company_id = res.scalars().one()
    
    # Update candidate ----------
    
    candidate_data = body.dict_candidate_only()
    candidate_data['creator_id'] = at.user_id
    
    stmt = update(m.Candidate).values(candidate_data).where(m.Candidate.id == candidate_id).returning(m.Candidate.id)
    res = await session.execute(stmt)
    
    try:
        _ = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    # ---------
    
    async def update_entities(model, entities_list):
        entities_ids = [entity.id for entity in entities_list if entity.id is not None]
        stmt = delete(model).where(model.id.not_in(entities_ids))
        res = await session.execute(stmt)
        for entity in entities_list:
            entity_dict = entity.dict(exclude_none=True)
            entity_dict['creator_id'] = at.user_id
            entity_dict['candidate_id'] = candidate_id
            stmt = insert(model) \
                .values(**entity_dict) \
                .on_conflict_do_update(index_elements=[model.id], set_=entity_dict)
            await session.execute(stmt)
    
    await update_entities(m.CandidateContact, body.contacts)
    await update_entities(m.CandidateWorkPlace, body.work_places)
    await update_entities(m.CandidateLanguageAbility, body.languages)
    await update_entities(m.CandidateNote, body.notes)
    
    existing_skills = [skill for skill in body.skills if isinstance(skill, sch.candidate.candidate_skill.Update)]
    
    new_skills_for_insert = []
    for skill in body.skills:
        if isinstance(skill, sch.candidate.skill.Create):
            new_skill_dict = skill.dict()
            new_skill_dict['normalized_name'] = skill.name.capitalize()
            new_skill_dict['company_id'] = company_id
            new_skills_for_insert.append(new_skill_dict)
            
    stmt = insert(m.Skill).values(new_skills_for_insert).returning(m.Skill.id)
    res = await session.execute(stmt)   
    new_skill_ids = res.scalars().all()
    
    existing_skills.extend([sch.candidate.candidate_skill.Update(skill_id=new_skill_id) for new_skill_id in new_skill_ids])
    
    await update_entities(m.CandidateSkill, existing_skills) 
    
    await session.commit()


@router.get('',
             name='Получение списка кандидатов',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetList.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
             )
async def get_list(query: Query = Depends(sch.GetList.Request.Query),
                   session: AsyncSession = Depends(get_session),
                   at: AccessToken = Depends(AccessJWTCookie())):
    
    stmt = select(m.Candidate) \
           .options(
               selectinload(m.Candidate.position),
               selectinload(m.Candidate.grade),
               selectinload(m.Candidate.adress),
               selectinload(m.Candidate.citizenship),
               selectinload(m.Candidate.family_status),
               selectinload(m.Candidate.contacts),
               selectinload(m.Candidate.languages),
               selectinload(m.Candidate.notes),
               selectinload(m.Candidate.skills),
               selectinload(m.Candidate.work_places),
               ) \
           .order_by(m.Candidate.created_at.desc())
           
    if query.first_name:
        stmt = stmt.filter(m.Candidate.first_name.ilike(f'%{query.first_name}%'))
        
    if query.last_name:
        stmt = stmt.filter(m.Candidate.last_name.ilike(f'%{query.last_name}%'))
        
    if query.middle_name:
        stmt = stmt.filter(m.Candidate.middle_name.ilike(f'%{query.middle_name}%'))
        
    if query.position_id:
        stmt = stmt.filter(m.Candidate.position_id == query.position_id)
        
    if query.recruiter_id:
        stmt = stmt.filter(m.Candidate.creator_id == query.recruiter_id)
           
    res = await session.execute(stmt)
    
    res_list = res.scalars().all()
    
    return sch.GetList.Response.Body(candidates=[sch.candidate.Read.from_orm(orm_model) for orm_model in res_list])
