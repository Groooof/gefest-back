import typing as tp
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete, update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import exc as sa_exc

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

from .repos import CandidatesRepo


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
    
    candidates_repo = CandidatesRepo(session)
    candidate_id = await candidates_repo.add(at.user_id, body)
    
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
             response_model=sch.Update.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
             )
async def update_candidate(id: UUID,
                           body: sch.Update.Request.Body,
                           session: AsyncSession = Depends(get_session),
                           at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Обновление данных кандидата
    '''
    
    candidates_repo = CandidatesRepo(session)
    try:
        candidate_id = await candidates_repo.update(id, at.user_id, body)
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    except sa_exc.IntegrityError:
        raise exc.InvalidRequestError
    
    return sch.Update.Response.Body(id=candidate_id)


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
