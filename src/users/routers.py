from fastapi import (
    APIRouter,
    Depends
)

import asyncpg

from .dto import Users as UsersDto
from ..service.roles import Roles
from ..service import exceptions as exc
from ..service.fastapi_custom import generate_openapi_responses
from ..service.dependencies import (
    AccessJWTCookie,
    CheckRoles,
    get_db_connection
)
from ..service.tokens import (
    AccessToken
)

from . import schemas as sch
from .repos import PostgresUsersRepo


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
                 con: asyncpg.Connection = Depends(get_db_connection),
                 at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Принимает данные для создания пользователя в теле запроса и вносит в бд<br>
    '''
    
    user_id = at.user_id
    users_repo = PostgresUsersRepo(con)
    create_data = UsersDto.Create.Input(creator_id=user_id, **body.dict())
    try:
        res = await users_repo.create(create_data)
    except asyncpg.exceptions.UniqueViolationError:
        raise exc.AlreadyExists
    
    return sch.Create.Response.Body(id=res.id)
