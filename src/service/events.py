from contextlib import asynccontextmanager

from .refs_loader import RefsLoader
from .database import database, engine, async_session
from .models import Base, Company, User, RoleRef
from ..config import postgres_env, POSTGRES_DSN
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert


async def on_startup() -> None:
    """
    Действия, выполняемые при запуске приложения
    """

    test_company = {'id': '00000000-0000-0000-0000-000000000000', 'full_name': 'ООО "ALMAX"', 'short_name': 'ALMAX', 'ogrn': '1234567890'}
    test_admin = {
        'id': '00000000-0000-0000-0000-000000000001',
        'username': 'admin',
        'password': 'admin',
        'role_code': 1,
        'company_id': '00000000-0000-0000-0000-000000000000',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'middle_name': 'Иванович',
        'email': 'vanya228@mail.ru'
        }
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        refs_loader = RefsLoader(conn)
        await refs_loader.load('./sql/refs.sql')
        await conn.execute(insert(Company).values(test_company).on_conflict_do_nothing())
        await conn.execute(insert(User).values(test_admin).on_conflict_do_nothing())
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
