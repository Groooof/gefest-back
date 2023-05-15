from src.database import database
from fastapi import Depends, Request, HTTPException
import asyncpg

from . import config
from .auth.service import AccessToken, RefreshToken, AccessTokenFactory, RefreshTokenFactory
from .public import exceptions as exc


class AccessJWTCookie:    
    def __init__(self, 
                 name: str = config.ACCESS_TOKEN_NAME,
                 check_expires: bool = True,
                 check_sign: bool = True
                 ) -> None:
        
        self._name = name
        self._check_exp = check_expires
        self._check_sign = check_sign
    
    def __call__(self, request: Request) -> AccessToken:
        raw_at = request.cookies.get(self._name)
        
        if raw_at is None:
            raise exc.InvalidTokenError
        
        at = AccessTokenFactory.fromstring(raw_at)
        
        is_valid = at.check_structure()
        if not is_valid:
            raise exc.InvalidTokenError
        
        if self._check_exp:
            is_valid = at.check_exp()
            if not is_valid:
                raise exc.ExpiredTokenError
            
        if self._check_sign:
            is_valid = at.check_sign(secret=config.jwt_env.SECRET, algorithm=config.JWT_ALG)
            if not is_valid:
                raise exc.InvalidTokenError
        return at
    
    
class RefreshUUIDCookie:
    def __init__(self, name: str = config.REFRESH_TOKEN_NAME) -> None:
        self._name = name
    
    def __call__(self, request: Request) -> RefreshToken:
        raw_rt = request.cookies.get(self._name)
        if raw_rt is None:
            raise exc.InvalidTokenError
        
        rt = RefreshTokenFactory.fromstring(raw_rt)
        is_valid = rt.check_structure()
        if not is_valid:
            raise exc.InvalidTokenError

        return rt


def get_db_connection(con: asyncpg.Connection = Depends(database.connection)):
    return con
