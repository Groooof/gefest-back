from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete, update
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import exc as sa_exc
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


router = APIRouter(tags=['roles'], prefix='/roles')


@router.post('',
             name='Список существующих ролей',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.GetRoles.Response.Body
             )
async def get_roles(session: AsyncSession = Depends(get_session),
                    at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Возвращает список существующих ролей в системе
    '''
    
    stmt = select(m.RoleRef)
    res = await session.execute(stmt)
    
    res_list = res.scalars().all()
    
    return sch.GetRoles.Response.Body(roles=[sch.RoleInfo.from_orm(orm_model) for orm_model in res_list])


@router.get('',
             name='test',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError,
                 exc.AccessDenied
                 ),
             dependencies=[Depends(CheckRoles(Roles.admin))]
             )
async def check_role():
    '''
    Тестовая ручка для проверки механизма ролевой модели доступа <br>
    *доступ к этой ручке имеет только админ
    '''
    return 'Yeey'
