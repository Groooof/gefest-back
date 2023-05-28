from contextlib import asynccontextmanager

from .refs_loader import RefsLoader
from .mocks_loader import MocksLoader
from .database import database, engine, async_session
from . import models as m
from ..config import postgres_env, POSTGRES_DSN
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert


async def on_startup() -> None:
    """
    Действия, выполняемые при запуске приложения
    """
    
    async with engine.begin() as conn:
        await conn.run_sync(m.Base.metadata.drop_all)
        await conn.run_sync(m.Base.metadata.create_all)
        
        refs_loader = RefsLoader(conn)
        await refs_loader.load('./data/refs.sql')
        mocks_loader = MocksLoader(conn)
        await mocks_loader.load()
        await conn.commit()
        
        
    # dsn = POSTGRES_DSN if POSTGRES_DSN is not None \
    #                    else get_postgres_dsn(postgres_env.USER, 
    #                                          postgres_env.PASSWORD, 
    #                                          postgres_env.HOST, 
    #                                          postgres_env.PORT, 
    #                                          postgres_env.DB)
    # await database.startup(dsn)
    
    # async with asynccontextmanager(database.connection)() as con:
    #     with open('init.sql') as f:
    #         await con.execute(f.read())


async def on_shutdown() -> None:
    """
    Действия, выполняемые при завершении работы приложения.
    """
    print('App is shutting down!')
