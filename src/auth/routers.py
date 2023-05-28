import datetime as dt

from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request
)

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import exc as sa_exc
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update
from sqlalchemy.future import select

from ..service.fastapi_custom import generate_openapi_responses
from ..service import exceptions as exc
from ..service import models as m
from .. import config
from ..service.dependencies import (
    AccessJWTCookie,
    RefreshUUIDCookie,
    get_session
)
from ..service.tokens import (
    AccessToken,
    RefreshToken,
    AccessTokenFactory,
    RefreshTokenFactory
)

from . import schemas as sch


router = APIRouter(tags=['sessions'], prefix='/sessions')


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
                 exc.InvalidClientError,
                 exc.AccountBlockedError
                 ),
             response_model=sch.Login.Response.Body
             )
async def login(response: Response,
                body: sch.Login.Request.Body,
                session: AsyncSession = Depends(get_session)):
    '''
    Принимает имя пользователя и пароль в теле запроса <br>
    В случае успешной аутентификации устанавливает access и refresh токены в куки
    '''
    
    stmt = select(m.User).where(m.User.username==body.username).limit(1).options(selectinload(m.User.role))
    res = await session.execute(stmt)
    
    try:
        user = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidClientError
    
    # if user.fails_count >= config.MAX_AUTH_FAILED_COUNT:
    #     raise exc.AccountBlockedError
    
    if user.password != body.password:
        # stmt = update(m.User).values(fails_count=user.fails_count + 1).where(m.User.id == user.id)
        # await session.execute(stmt)
        # await session.commit()
        raise exc.InvalidClientError

    at = AccessTokenFactory.create(user.id, user.role.sys_name, user.company_id)    
    rt = RefreshTokenFactory.create()
    
    stmt = insert(m.RefreshToken).values(user_id=user.id, token=str(rt), expires_at=dt.datetime.now() + config.REFRESH_TOKEN_LIFETIME)
    res = await session.execute(stmt)
    await session.commit()
    
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
    return sch.Login.Response.Body(user_id=user.id, role_code=user.role.code)


@router.delete('',
               name='Выход из системы',
               responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError
                   )
               )
async def logout(response: Response,
                 session: AsyncSession = Depends(get_session),
                 at: AccessToken = Depends(AccessJWTCookie(check_expires=False)),
                 rt: RefreshToken = Depends(RefreshUUIDCookie())):
    '''
    Для организации правильного выхода необходим access и refresh токены в куках <br>
    access токен может быть просрочен, главное - его наличие <br>
    В случае успешного выхода оба токена удаляются из кук
    '''
    
    stmt = delete(m.RefreshToken).where(
        (m.RefreshToken.user_id == at.user_id) 
        & 
        (m.RefreshToken.token == str(rt))
        &
        (m.RefreshToken.expires_at >= dt.datetime.now())
    ).returning(m.RefreshToken.token)
    res = await session.execute(stmt)
    
    try:
        token = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidTokenError
    
    await session.commit()
    
    response.delete_cookie(config.ACCESS_TOKEN_NAME)
    response.delete_cookie(config.REFRESH_TOKEN_NAME)
    response.status_code = 200


@router.patch('',
              name='Обновление токенов',
              responses=generate_openapi_responses(
                   exc.InvalidRequestError,
                   exc.InvalidTokenError
                   )
              )
async def refresh(response: Response,
                  session: AsyncSession = Depends(get_session),
                  at: AccessToken = Depends(AccessJWTCookie(check_expires=False)),
                  rt: RefreshToken = Depends(RefreshUUIDCookie())):
    '''
    Для организации правильного обновления токенов необходимы access и refresh токены в куках <br>
    access токен может быть просрочен, главное - его наличие <br>
    В случае успешного обновления в куки устанавливаются новые access и refresh токены
    '''
    
    new_at = AccessTokenFactory.create(at.user_id, at.role)
    new_rt = RefreshTokenFactory.create()    

    stmt = update(m.RefreshToken) \
           .where(
               (m.RefreshToken.user_id == at.user_id) 
               & 
               (m.RefreshToken.token == str(rt))
               &
               (m.RefreshToken.expires_at >= dt.datetime.now())) \
           .values(token=str(new_rt), expires_at=dt.datetime.now() + config.REFRESH_TOKEN_LIFETIME) \
           .returning(m.RefreshToken.token)
           
    res = await session.execute(stmt)
    await session.commit()
    
    try:
        token = res.scalars().one()
    except sa_exc.NoResultFound:
        raise exc.InvalidTokenError
    
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
