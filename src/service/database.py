from abc import ABCMeta, abstractmethod
import typing as tp
import asyncpg

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config import postgres_env, POSTGRES_DSN


def get_dsn(user: str, password: str, host: str, port: str, db: str, prefix: str = 'postgres'):
    dsn_without_prefix = f'{user}:{password}@{host}:{port}/{db}'
    return prefix + '://' + dsn_without_prefix


def parse_dokku_dsn(dsn: str):
    dsn_without_prefix = dsn.split('://')[1]
    user = dsn_without_prefix.split(':')[0]
    password = dsn_without_prefix.split(':')[1].split('@')[0]
    host = dsn_without_prefix.split('@')[1].split(':')[0]
    port = dsn_without_prefix.split(':')[2].split('/')[0]
    db = dsn_without_prefix.split('/')[1]
    return user, password, host, port, db


sa_prefix = 'postgresql+asyncpg'
if POSTGRES_DSN is None:
    DATABASE_URL = get_dsn(postgres_env.USER,
                           postgres_env.PASSWORD,
                           postgres_env.HOST,
                           postgres_env.PORT,
                           postgres_env.DB,
                           sa_prefix)
else:
    DATABASE_URL = get_dsn(*parse_dokku_dsn(POSTGRES_DSN), sa_prefix)


engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class IDatabase(metaclass=ABCMeta):

    @abstractmethod
    async def startup(self, dsn: str) -> None:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass

    @abstractmethod
    async def connection(self):
        pass


class ASPGDatabase(IDatabase):
    def __init__(self):
        self.pool: tp.Optional[asyncpg.Pool] = None

    async def startup(self, dsn: str) -> None:
        """
        Создание асинхронного пула подключений к бд.
        """
        self.pool = await asyncpg.create_pool(dsn, timeout=5)

    async def shutdown(self) -> None:
        """
        Закрытие пула подключений.
        """
        await self.pool.close()

    async def connection(self) -> asyncpg.Connection:
        """
        Получение подключения из пула.
        """
        if self.pool is None:
            raise NotImplementedError('DB pool must be created first')
        con = await self.pool.acquire()
        try:
            yield con
        finally:
            await self.pool.release(con)


database = ASPGDatabase()
