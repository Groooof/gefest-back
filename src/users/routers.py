from uuid import UUID
import typing as tp
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
from ..service import exceptions as exc
from ..service.fastapi_custom import generate_openapi_responses
from ..service.dependencies import (
    AccessJWTCookie,
    CheckRoles,
    get_session
)
from ..service.tokens import (
    AccessToken
)

from . import schemas as sch


router = APIRouter(tags=['users'], prefix='/users')


@router.post('',
             name='Создание пользователя',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied,
                 exc.AlreadyExists
                 ),
             response_model=sch.Create.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.admin))]
             )
async def create(body: sch.Create.Request.Body,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Принимает данные для создания пользователя в теле запроса и вносит в бд <br>
    '''
    
    stmt = select(m.User.company_id).where(m.User.id == at.user_id)
    res = await session.execute(stmt)
    company_id = res.scalars().one()
    
    stmt = insert(m.User).values(creator_id=at.user_id, company_id=company_id, **body.dict()).returning(m.User.id)
    try:
        res = await session.execute(stmt)
        await session.commit()
    except sa_exc.IntegrityError:
        raise exc.AlreadyExists
        
    user_id = res.scalars().one()
    return sch.Create.Response.Body(id=user_id)


@router.get('/current',
             name='Получение информации о текущем пользователе',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 ),
             response_model=sch.GetSelfInfo.Response.Body
             )
async def get_self_info(session: AsyncSession = Depends(get_session),
                        at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Возвращает данные о пользователе, который авторизован в данный момент <br>
    '''
    
    stmt = select(m.User) \
           .where(m.User.id == at.user_id) \
           .options(
               selectinload(m.User.department),
               selectinload(m.User.position),
               selectinload(m.User.grade)
            )
    res = await session.execute(stmt)
    
    try:
        user = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
        
    return sch.GetSelfInfo.Response.Body.from_orm(user)


@router.get('/{id}',
             name='Получение информации о пользователе с указанным id',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied
                 ),
             response_model=sch.GetUserInfo.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.admin))]
             )
async def get_user_info(id: UUID,
                        session: AsyncSession = Depends(get_session),
                        at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Возвращает данные о пользователе <br>
    '''
    
    stmt = select(m.User) \
           .where(m.User.id == id) \
           .options(
               selectinload(m.User.department),
               selectinload(m.User.position),
               selectinload(m.User.grade)
            )
    res = await session.execute(stmt)
    
    try:
        user = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.GetUserInfo.Response.Body.from_orm(user)


@router.get('',
             name='Получение информации о всех пользователях текущей компании',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied
                 ),
             response_model=sch.GetCompanyUsersInfo.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.admin))]
             )
async def get_company_users_info(session: AsyncSession = Depends(get_session),
                                 at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Возвращает данные всех пользователях <br>
    '''
    
    current_company_id = select(m.User.company_id) \
                         .where(m.User.id == at.user_id) \
                         .scalar_subquery()
    stmt = select(m.User) \
           .where(m.User.company_id == current_company_id) \
           .options(
               selectinload(m.User.department),
               selectinload(m.User.position),
               selectinload(m.User.grade)
            )
    
    res = await session.execute(stmt)
    
    res_list = res.scalars().all()
    
    return sch.GetCompanyUsersInfo.Response.Body(users=[sch.user.Read.from_orm(orm_model) for orm_model in res_list])


@router.delete('/{id}',
               name='Удаление пользователя',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError,
                   exc.ExpiredTokenError,
                   exc.InvalidClientError,
                   exc.AccessDenied
                   ),
               response_model=sch.DeleteUser.Response.Body,
               dependencies=[Depends(CheckRoles(Roles.admin))]
               )
async def delete_user(id: UUID,
                      session: AsyncSession = Depends(get_session),
                      at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Удаляет пользователя с указанным id
    '''
    
    stmt = delete(m.User).where(m.User.id == id).returning(m.User.id)
    res = await session.execute(stmt)
    
    try:
        user_id = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    await session.commit()
    
    return sch.DeleteUser.Response.Body(id=user_id)
