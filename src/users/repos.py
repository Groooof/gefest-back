from abc import ABC, abstractmethod
import typing as tp
import asyncpg

from . import dto


class UsersRepo(ABC):
    
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def verify(self):
        pass


class PostgresUsersRepo(UsersRepo):
    _db_table = 'users'
    
    def __init__(self, con: asyncpg.Connection) -> None:
        self._con = con

    async def create(self, data: dto.Users.Create.Input) -> tp.Optional[dto.Users.Create.Output]:
        query = f'''
        INSERT INTO {self._db_table}
        (
            username,
            hashed_password,
            role_code,
            company_id,
            department_id,
            position_id,
            grade_id,
            first_name,
            last_name,
            middle_name,
            email,
            creator_id
        )
        VALUES ($1, crypt($2, gen_salt('bf', 10)), $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING id
        '''
        res = await self._con.fetchval(query, *data.dict().values())
        return dto.Users.Create.Output(id=res) if res is not None else None
    
    async def verify(self, data: dto.Users.Verify.Input) -> tp.Optional[dto.Users.Verify.Output]:
        query = f'''
        SELECT u.id, u.role_code, r.sys_name AS role_sys_name
        FROM {self._db_table} u
        JOIN refs.roles r ON r.code = u.role_code
        WHERE u.username=$1 AND u.hashed_password = crypt($2, u.hashed_password);
        '''
        res = await self._con.fetchrow(query, data.username, data.password)
        return dto.Users.Verify.Output(**res) if res is not None else None