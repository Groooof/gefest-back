from contextlib import asynccontextmanager

from .database import database
from ..config import postgres_env, POSTGRES_DSN


def get_postgres_dsn(user: str, password: str, host: str, port: str, db: str,
                     sa_driver: str = None, sa_dialect: str = None):
    """
    Генерация ссылки для подключения к бд.
    """
    dsn_without_prefix = f'{user}:{password}@{host}:{port}/{db}'

    if sa_driver is None and sa_dialect is None:
        base_prefix = 'postgres://'
        return base_prefix + dsn_without_prefix

    sa_prefix = f'{sa_driver}+{sa_dialect}://'
    return sa_prefix + dsn_without_prefix


async def on_startup() -> None:
    """
    Действия, выполняемые при запуске приложения
    """
    dsn = POSTGRES_DSN if POSTGRES_DSN is not None \
                       else get_postgres_dsn(postgres_env.USER, 
                                             postgres_env.PASSWORD, 
                                             postgres_env.HOST, 
                                             postgres_env.PORT, 
                                             postgres_env.DB)
    await database.startup(dsn)
    
    async with asynccontextmanager(database.connection)() as con:
        with open('init.sql') as f:
            await con.execute(f.read())


async def on_shutdown() -> None:
    """
    Действия, выполняемые при завершении работы приложения.
    """
    print('App is shutting down!')
