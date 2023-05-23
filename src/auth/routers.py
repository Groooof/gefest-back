import datetime as dt

from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request
)

import asyncpg

from ..users.repos import PostgresUsersRepo
from ..users.dto import Users as UsersDto
from .. import config
from ..service import exceptions as exc
from ..service.fastapi_custom import generate_openapi_responses
from ..service.dependencies import (
    AccessJWTCookie,
    RefreshUUIDCookie,
    get_db_connection
)
from ..service.tokens import (
    AccessToken,
    RefreshToken,
    AccessTokenFactory,
    RefreshTokenFactory
)

from .dto import RefreshToken as RefreshTokenDto
from .repos import PostgresRefreshTokenRepo
from . import schemas as sch



router = APIRouter(tags=['users'], prefix='/session')


@router.post('/protected',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError
                 )
             )
async def protected(request: Request,
                    at: AccessToken = Depends(AccessJWTCookie()),
                    rt: RefreshToken = Depends(RefreshUUIDCookie())):
    
    
    return 'welcome 2z club body'


@router.post('',
             name='Аутентификация пользователя',
             responses=generate_openapi_responses(
                 exc.InvalidRequestError,
                 exc.InvalidTokenError,
                 exc.ExpiredTokenError,
                 exc.InvalidClientError
                 ),
             response_model=sch.Login.Response.Body
             )
async def login(response: Response,
                body: sch.Login.Request.Body,
                con: asyncpg.Connection = Depends(get_db_connection)):
    '''
    Принимает имя пользователя и пароль в теле запроса <br>
    В случае успешной аутентификации устанавливает access и refresh токены в куки
    '''
    u_repo = PostgresUsersRepo(con)
    
    verify_data = UsersDto.Verify.Input(username=body.username, password=body.password)
    res = await u_repo.verify(verify_data)
    if res is None:
        raise exc.InvalidClientError
    
    at = AccessTokenFactory.create(res.id, res.role_sys_name)    
    rt = RefreshTokenFactory.create()

    rt_repo = PostgresRefreshTokenRepo(con)
    create_data = RefreshTokenDto.Create.Input(user_id=res.id,
                                               token=str(rt),
                                               expires_at=dt.datetime.now() + config.REFRESH_TOKEN_LIFETIME)
    await rt_repo.create(create_data)
    
    response.set_cookie(config.ACCESS_TOKEN_NAME, 
                        str(at),
                        max_age=int(config.REFRESH_TOKEN_LIFETIME.total_seconds()),
                        secure=True,
                        httponly=True,
                        samesite='none')
    response.set_cookie(config.REFRESH_TOKEN_NAME,
                        str(rt),
                        max_age=int(config.REFRESH_TOKEN_LIFETIME.total_seconds()),
                        secure=True,
                        httponly=True,
                        samesite='none')
    response.status_code = 200
    return sch.Login.Response.Body(user_id=res.id, role_code=res.role_code)


@router.delete('',
               name='Выход из системы',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError
                   )
               )
async def logout(response: Response,
                 con: asyncpg.Connection = Depends(get_db_connection),
                 at: AccessToken = Depends(AccessJWTCookie(check_expires=False)),
                 rt: RefreshToken = Depends(RefreshUUIDCookie())):
    '''
    Для организации правильного выхода необходим access и refresh токены в куках <br>
    access токен может быть просрочен, главное - его наличие <br>
    В случае успешного выхода оба токена удаляются из кук
    '''
    
    rt_repo = PostgresRefreshTokenRepo(con)
    
    # проверяем в бд принадлежит ли refresh token данному пользователю
    verify_data = RefreshTokenDto.Verify.Input(user_id=at.user_id, token=str(rt))
    is_valid = await rt_repo.verify(verify_data)
    if not is_valid:
        raise exc.InvalidTokenError

    # удаляем токен из бд
    del_data = RefreshTokenDto.Delete.Input(token=str(rt))
    await rt_repo.delete(del_data)
    
    response.delete_cookie('at')
    response.delete_cookie('rt')
    response.status_code = 200


@router.patch('',
              name='Обновление токенов',
              responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError
                   )
              )
async def refresh(response: Response,
                  con: asyncpg.Connection = Depends(get_db_connection),
                  at: AccessToken = Depends(AccessJWTCookie(check_expires=False)),
                  rt: RefreshToken = Depends(RefreshUUIDCookie())):
    '''
    Для организации правильного обновления токенов необходимы access и refresh токены в куках <br>
    access токен может быть просрочен, главное - его наличие <br>
    В случае успешного обновления в куки устанавливаются новые access и refresh токены
    '''
    
    rt_repo = PostgresRefreshTokenRepo(con)
    
    # проверяем в бд принадлежит ли refresh token данному пользователю
    verify_data = RefreshTokenDto.Verify.Input(user_id=at.user_id, token=str(rt))
    is_valid = await rt_repo.verify(verify_data)
    if not is_valid:
        raise exc.InvalidTokenError
    
    # генерируем новые токены
    new_at = AccessTokenFactory.create(at.user_id, at.role)
    new_rt = RefreshTokenFactory.create()
    
    # заменяем в бд старый токен на новый
    update_data = RefreshTokenDto.Update.Input(token=str(rt),
                                               new_token=str(new_rt),
                                               new_expires_at=dt.datetime.now() + config.REFRESH_TOKEN_LIFETIME)
    await rt_repo.update(update_data)
    
    response.set_cookie(config.ACCESS_TOKEN_NAME, 
                        str(new_at),
                        max_age=int(config.REFRESH_TOKEN_LIFETIME.total_seconds()),
                        secure=True,
                        httponly=True,
                        samesite='none')
    response.set_cookie(config.REFRESH_TOKEN_NAME,
                        str(new_rt),
                        max_age=int(config.REFRESH_TOKEN_LIFETIME.total_seconds()),
                        secure=True,
                        httponly=True,
                        samesite='none')
    response.status_code = 200
