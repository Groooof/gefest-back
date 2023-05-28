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

    test_company = {'id': '00000000-0000-0000-0000-000000000000', 'full_name': 'ООО "ALMAX"', 'short_name': 'ALMAX', 'ogrn': '1234567890'}
    test_departments = [
        {'id': '00000000-0000-0000-0000-000000000002', 'name': 'Отдел разработки', 'company_id': '00000000-0000-0000-0000-000000000000'},
        {'id': '00000000-0000-0000-0000-000000000003', 'name': 'Отдел аналитики', 'company_id': '00000000-0000-0000-0000-000000000000'},
        {'id': '00000000-0000-0000-0000-000000000004', 'name': 'Отдел администрирования', 'company_id': '00000000-0000-0000-0000-000000000000'}
        ]
    test_positions = [
        {'id': '00000000-0000-0000-0000-000000000005', 'name': 'Python-developer', 'company_id': '00000000-0000-0000-0000-000000000000'},
        {'id': '00000000-0000-0000-0000-000000000006', 'name': 'DepOps-engineer', 'company_id': '00000000-0000-0000-0000-000000000000'},
        {'id': '00000000-0000-0000-0000-000000000007', 'name': 'Frontend-developer', 'company_id': '00000000-0000-0000-0000-000000000000'}
        ]
    test_grades = [
        {'id': '00000000-0000-0000-0000-000000000008', 'name': 'Junior', 'company_id': '00000000-0000-0000-0000-000000000000'},
        {'id': '00000000-0000-0000-0000-000000000009', 'name': 'Middle', 'company_id': '00000000-0000-0000-0000-000000000000'},
        {'id': '00000000-0000-0000-0000-000000000010', 'name': 'Senior', 'company_id': '00000000-0000-0000-0000-000000000000'}
    ]
    test_admin = {
        'id': '00000000-0000-0000-0000-000000000001',
        'username': 'admin',
        'password': 'admin',
        'role_code': 1,
        'company_id': '00000000-0000-0000-0000-000000000000',
        'department_id': '00000000-0000-0000-0000-000000000004',
        'position_id': '00000000-0000-0000-0000-000000000006',
        'grade_id': '00000000-0000-0000-0000-000000000010',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'middle_name': 'Иванович',
        'email': 'vanya228@mail.ru'
        }
    test_skills = [
        {'id': '00000000-0000-0000-0000-000000000011', 'name': 'Python', 'normalized_name': 'Python', 'company_id': '00000000-0000-0000-0000-000000000000'},
        {'id': '00000000-0000-0000-0000-000000000012', 'name': 'Docker', 'normalized_name': 'Docker', 'company_id': '00000000-0000-0000-0000-000000000000'},
        {'id': '00000000-0000-0000-0000-000000000013', 'name': 'JavaScript', 'normalized_name': 'JavaScript', 'company_id': '00000000-0000-0000-0000-000000000000'}
    ]
    
    async with engine.begin() as conn:
        # await conn.run_sync(m.Base.metadata.drop_all)
        # await conn.run_sync(m.Base.metadata.create_all)
        refs_loader = RefsLoader(conn)
        await refs_loader.load('./data/refs.sql')
        mocks_loader = MocksLoader(conn)
        await mocks_loader.load()
        await conn.execute(insert(m.Company).values(test_company).on_conflict_do_nothing())
        await conn.execute(insert(m.Department).values(test_departments).on_conflict_do_nothing())
        await conn.execute(insert(m.Position).values(test_positions).on_conflict_do_nothing())
        await conn.execute(insert(m.Grade).values(test_grades).on_conflict_do_nothing())
        await conn.execute(insert(m.User).values(test_admin).on_conflict_do_nothing())
        await conn.execute(insert(m.Skill).values(test_skills).on_conflict_do_nothing())
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
