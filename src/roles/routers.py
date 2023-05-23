from fastapi import (
    APIRouter,
    Depends
)

import asyncpg

from .repos import PostgresRolesRepo
from ..service.roles import Roles
from ..service.dependencies import (
    AccessJWTCookie,
    RefreshUUIDCookie,
    CheckRoles,
    get_db_connection
)

from . import schemas as sch
from ..service.tokens import (
    AccessToken,
    RefreshToken
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
async def get_roles(con: asyncpg.Connection = Depends(get_db_connection),
                    at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Возвращает список существующих ролей в системе
    '''
    roles_repo = PostgresRolesRepo(con)
    res = await roles_repo.get_all()
    
    roles_list = [sch.RoleInfo(code=role.code, name=role.name, sys_name=role.sys_name) for role in res.roles]
    return sch.GetRoles.Response.Body(roles=roles_list)


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
