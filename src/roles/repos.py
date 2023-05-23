from abc import ABC, abstractmethod

import asyncpg

from . import dto


class RolesRepo(ABC):
    
    @abstractmethod
    def get_all(self):
        pass


class PostgresRolesRepo(RolesRepo):
    _db_table = 'refs.roles'
    
    def __init__(self, con: asyncpg.Connection) -> None:
        self._con = con
        
    async def get_all(self) -> dto.Roles.GetAll.Output:
        query = f'''
        SELECT code, name, sys_name FROM {self._db_table};
        '''
        res = await self._con.fetch(query)
        print(res)
        return dto.Roles.GetAll.Output(roles=[dto.RoleInfo(**row) for row in res])
