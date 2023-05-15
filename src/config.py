from pydantic import BaseSettings
import datetime as dt
import pathlib


class BaseEnv(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PostgresEnv(BaseEnv):
    """
    Переменные окружения.
    """
    USER: str
    PASSWORD: str
    DB: str
    HOST: str
    PORT: str

    class Config:
        env_prefix = 'POSTGRES_'


class JWTEnv(BaseEnv):
    SECRET: str

    class Config:
        env_prefix = 'JWT_'
    

postgres_env = PostgresEnv()
POSTGRES_DSN = os.environ.get('DATABASE_URL')
jwt_env = JWTEnv()

JWT_ALG = 'HS256'

ACCESS_TOKEN_NAME = 'at'
REFRESH_TOKEN_NAME = 'rt'

ACCESS_TOKEN_LIFETIME = dt.timedelta(minutes=59)
# ACCESS_TOKEN_LIFETIME = dt.timedelta(seconds=5)
REFRESH_TOKEN_LIFETIME = dt.timedelta(days=7)
