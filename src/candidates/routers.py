import typing as tp
import datetime as dt
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
    try:
        candidate_id = await candidates_repo.add(at.user_id, body)
    except sa_exc.IntegrityError:
        raise exc.InvalidClientError
    
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


@router.get('/{id}',
             name='Получение данных кандидата',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetOne.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
             )
async def get_one(id: UUID,
                  session: AsyncSession = Depends(get_session),
                  at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Получение данных о кандидате с указанным id
    '''
    
    candidates_repo = CandidatesRepo(session)
    try:
        candidate = await candidates_repo.get_one(id, at.company_id)
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    total_exp = 0
    for place in candidate.work_places:
        exp = (place.work_to or dt.datetime.now()) - place.work_from
        total_exp += exp.days
    candidate.total_work_expirience = f'{total_exp // 365} {total_exp % 365 // 30}'
        
    return sch.GetOne.Response.Body(**candidate.dict())


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
    '''
    Получение списка кандидатов в текущей компании с фильтрами и сортировкой
    '''
    
    candidates_repo = CandidatesRepo(session)
    candidates = await candidates_repo.get_list(company_id=at.company_id, **query.dict())
    for candidate in candidates:
        total_exp = 0
        for place in candidate.work_places:
            exp = (place.work_to or dt.datetime.now()) - place.work_from
            total_exp += exp.days
        candidate.total_work_expirience = f'{total_exp // 365} {total_exp % 365 // 30}'
    return sch.GetList.Response.Body(candidates=candidates, count=len(candidates))


@router.delete('/{id}',
               name='Удаление кандидата',
                responses=generate_openapi_responses(
                    exc.InvalidRequestError,
                    exc.InvalidTokenError,
                    exc.ExpiredTokenError,
                    exc.InvalidClientError
                    ),
                response_model=sch.Delete.Response.Body,
                dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter, Roles.admin))]
                )
async def delete(id: UUID,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Удаление кандидата с указанным id
    '''
    
    candidates_repo = CandidatesRepo(session)
    try:
        candidate_id = await candidates_repo.delete(id, at.company_id)
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.Delete.Response.Body(id=candidate_id)
