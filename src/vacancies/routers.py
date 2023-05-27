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

from .repos import VacanciesRepo


router = APIRouter(tags=['vacancies'], prefix='/vacancies')


@router.post('',
             name='Создание вакансии (заявки)',
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
    Добавляет вакансию в систему
    '''
    
    vacancies_repo = VacanciesRepo(session)
    try:
        vacancy_id = await vacancies_repo.add(at.user_id, body)
    except sa_exc.IntegrityError:
        raise exc.InvalidRequestError
    
    return sch.Create.Response.Body(id=vacancy_id)


@router.patch('/{id}',
             name='Обновление данных вакансии',
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
    Обновление данных вакансии
    '''
    
    vacancies_repo = VacanciesRepo(session)
    try:
        vacancy_id = await vacancies_repo.update(id, at.user_id, body)
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    except sa_exc.IntegrityError:
        raise exc.InvalidRequestError
    
    return sch.Update.Response.Body(id=vacancy_id)


@router.get('/{id}',
             name='Получение данных вакансии',
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
    Получение данных о вакансии с указанным id
    '''
    
    vacancies_repo = VacanciesRepo(session)
    try:
        vacancy = await vacancies_repo.get_one(id, at.company_id)
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.GetOne.Response.Body(**vacancy.dict())


@router.get('',
             name='Получение списка вакансий',
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
    Получение списка вакансий в текущей компании с фильтрами и сортировкой
    '''
    
    vacancies_repo = VacanciesRepo(session)
    vacancies = await vacancies_repo.get_list(company_id=at.company_id, filters=query)
    return sch.GetList.Response.Body(vacancies=vacancies, count=len(vacancies))


@router.delete('/{id}',
               name='Удаление вакансии',
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
    Удаление вакансии с указанным id
    '''
    
    vacancies_repo = VacanciesRepo(session)
    try:
        vacancy_id = await vacancies_repo.delete(id, at.company_id)
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.Delete.Response.Body(id=vacancy_id)
