from uuid import UUID
from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.dialects.postgresql import insert as _insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as _select
from sqlalchemy import delete as _delete
from sqlalchemy import update as _update
from sqlalchemy.orm import selectinload
from sqlalchemy import exc as sa_exc


from ..service.fastapi_custom import generate_openapi_responses
from ..service import exceptions as exc
from ..service.roles import Roles
from ..service import models as m
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
    
    stmt = _insert(m.User) \
           .values(creator_id=at.user_id, company_id=at.company_id, **body.dict()) \
           .returning(m.User.id)
           
    try:
        user_id = (await session.scalars(stmt)).one()
        await session.commit()
    except sa_exc.IntegrityError:
        raise exc.AlreadyExists
        
    return sch.Create.Response.Body(id=user_id)


@router.get('/current',
            name='Получение информации о текущем пользователе',
            responses=generate_openapi_responses(
                exc.InvalidRequestError,
                exc.InvalidTokenError,
                exc.ExpiredTokenError,
                exc.InvalidClientError,
                ),
            response_model=sch.GetSelf.Response.Body
            )
async def get_self(session: AsyncSession = Depends(get_session),
                   at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Возвращает данные о пользователе, который авторизован в данный момент <br>
    '''
    
    stmt = _select(m.User).where(m.User.id == at.user_id)

    try:
        user = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
        
    return sch.GetSelf.Response.Body.from_orm(user)


@router.get('/{id}',
            name='Получение информации о пользователе с указанным id',
            responses=generate_openapi_responses(
                exc.InvalidRequestError,
                exc.InvalidTokenError,
                exc.ExpiredTokenError,
                exc.InvalidClientError,
                exc.AccessDenied
                ),
            response_model=sch.GetOne.Response.Body,
            dependencies=[Depends(CheckRoles(Roles.admin))]
            )
async def get_one(id: UUID,
                  session: AsyncSession = Depends(get_session),
                  at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Возвращает данные о пользователе <br>
    '''
    
    stmt = _select(m.User).where(m.User.id == id)
           
    try:
        user = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.GetOne.Response.Body.from_orm(user)


@router.get('',
            name='Получение информации о всех пользователях текущей компании',
            responses=generate_openapi_responses(
                exc.InvalidRequestError,
                exc.InvalidTokenError,
                exc.ExpiredTokenError,
                exc.InvalidClientError,
                exc.AccessDenied
                ),
            response_model=sch.GetList.Response.Body,
            dependencies=[Depends(CheckRoles(Roles.admin))]
            )
async def get_list(session: AsyncSession = Depends(get_session),
                   at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Возвращает данные о всех пользователях <br>
    '''
    
    stmt = _select(m.User).where(m.User.company_id == at.company_id)
    res = await session.scalars(stmt)
    users = [sch.user.Read.from_orm(orm_model) for orm_model in res.all()]
    return sch.GetList.Response.Body(users=users)


@router.delete('/{id}',
               name='Удаление пользователя',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError,
                   exc.ExpiredTokenError,
                   exc.InvalidClientError,
                   exc.AccessDenied
                   ),
               response_model=sch.Delete.Response.Body,
               dependencies=[Depends(CheckRoles(Roles.admin))]
               )
async def delete(id: UUID,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Удаляет пользователя с указанным id
    '''
    
    stmt = _delete(m.User) \
          .where(m.User.id == id) \
          .where(m.User.company_id == at.company_id) \
          .returning(m.User.id)
    
    try:
        user_id = (await session.scalars(stmt)).one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    return sch.Delete.Response.Body(id=user_id)
