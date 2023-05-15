from abc import ABC, abstractmethod

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

    async def create(self, data: dto.Users.Create.Input) -> dto.Users.Create.Output:
        query = f'''
        INSERT INTO {self._db_table} (username, hashed_password, role, is_superuser)
        VALUES ($1, crypt($2, gen_salt('bf', 10)), $3, $4)
        RETURNING id
        '''
        res = await self._con.fetchval(query, data.username, data.password, data.role, data.is_superuser)
        return dto.Users.Create.Output(id=res)
    
    async def verify(self, data: dto.Users.Verify.Input) -> dto.Users.Verify.Output:
        query = f'''
        SELECT id FROM {self._db_table} WHERE username=$1 AND hashed_password = crypt($2, hashed_password);
        '''
        res = await self._con.fetchval(query, data.username, data.password)
        return dto.Users.Verify.Output(id=res)
