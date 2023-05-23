import datetime as dt
import typing as tp
import uuid

import jwt

from .. import config


class UUIDToken:
    def __init__(self, token: str) -> None:
        self._token = token

    def check_structure(self) -> bool:
        try:
            uuid.UUID(self._token)
        except ValueError:
            return False
        return True
    
    def __str__(self) -> str:
        return self._token
        

class JWTToken:
    def __init__(self, token) -> None:
        self._token = token

    def check_structure(self) -> bool:
        options = {"verify_signature": False,
                   'verify_exp': False}
        try:
            jwt.decode(self._token, options=options)
        except jwt.DecodeError:
            return False
        return True

    def check_exp(self) -> bool:
        options = {"verify_signature": False,
                   'verify_exp': True}
        try:
            jwt.decode(self._token, options=options)
        except jwt.ExpiredSignatureError:
            return False
        return True

    def check_sign(self, secret: str, algorithm: str) -> bool:        
        options = {"verify_signature": True,
                   'verify_exp': False}
        try:
            jwt.decode(self._token,
                       algorithms=[algorithm] if algorithm is not None else None,
                       key=secret,
                       options=options)
        except jwt.InvalidSignatureError:
            return False
        return True

    def decode(self) -> dict:
        options = {"verify_signature": False,
                   'verify_exp': False}
        return jwt.decode(self._token, options=options)

    def __str__(self) -> str:
        return self._token


class UUIDTokenFactory:
    @staticmethod
    def create() -> UUIDToken:
        token = str(uuid.uuid4())
        return UUIDToken(token)

    @staticmethod
    def fromstring(token: str, check_structure=True) -> UUIDToken:
        uuid_token = UUIDToken(token)
        is_valid = uuid_token.check_structure()
        if check_structure and not is_valid:
            raise Exception('Invalid token structure')
        return uuid_token


class JWTTokenFactory:
    @staticmethod
    def create(secret: str, algorithm: str = 'HS256', **payload) -> str:
        token = jwt.encode(payload, key=secret, algorithm=algorithm)
        return JWTToken(token)

    @staticmethod
    def fromstring(token: str, check_structure=True) -> JWTToken:
        jwt_token = JWTToken(token)
        is_valid = jwt_token.check_structure()
        if check_structure and not is_valid:
            raise Exception('Invalid token structure')
        return jwt_token


class AccessToken(JWTToken):
    @property
    def user_id(self):
        return self.decode()['sub']
    
    @property
    def role(self):
        return self.decode()['role']


class RefreshToken(UUIDToken):
    pass


class RefreshTokenFactory(UUIDTokenFactory):
    @classmethod
    def create(cls) -> RefreshToken:
        uuid_token = super().create()
        token = str(uuid_token)
        return RefreshToken(token)

    @classmethod
    def fromstring(cls, token: str, check_structure=False) -> RefreshToken:
        uuid_token = super().fromstring(token, check_structure)
        token = str(uuid_token)
        return RefreshToken(token)


class AccessTokenFactory(JWTTokenFactory):
    @classmethod
    def create(cls, user_id: tp.Union[str, uuid.UUID], role: str) -> AccessToken:
        kwargs = {}
        kwargs['secret'] = config.jwt_env.SECRET
        kwargs['algorithm'] = 'HS256'
        kwargs['sub'] = str(user_id)
        kwargs['role'] = role
        kwargs['exp'] = dt.datetime.now(tz=dt.timezone.utc) + config.ACCESS_TOKEN_LIFETIME
        jwt_token = super().create(**kwargs)
        token = str(jwt_token)
        return AccessToken(token)

    @classmethod
    def fromstring(cls, token: str, check_structure=False) -> AccessToken:
        jwt_token = super().fromstring(token, check_structure)
        token = str(jwt_token)
        return AccessToken(token)
    
    