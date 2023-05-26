from fastapi import (
    APIRouter,
    Depends
)

import asyncpg

# from .repos import PostgresRolesRepo
from ..service.roles import Roles
from ..service.dependencies import (
    AccessJWTCookie,
    CheckRoles,
    get_db_connection
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
            #  response_model=sch.Create.Response.Body,
             dependencies=[Depends(CheckRoles(Roles.manager, Roles.recruiter))]
             )
async def create(body: sch.Create.Request.Body,
                 con: asyncpg.Connection = Depends(get_db_connection),
                 at: AccessToken = Depends(AccessJWTCookie())):
    '''
    Добавляет кандидата в систему
    '''
    
    from pprint import pprint
    pprint(body.dict())



