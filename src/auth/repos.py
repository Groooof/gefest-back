from abc import ABC, abstractmethod

import asyncpg

from . import dto


class RefreshTokenRepo(ABC):
    
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    
    @abstractmethod
    def verify(self):
        pass


class PostgresRefreshTokenRepo(RefreshTokenRepo):
    _db_table = 'refresh_tokens'
    
    def __init__(self, con: asyncpg.Connection) -> None:
        self._con = con

    async def create(self, data: dto.RefreshToken.Create.Input) -> None:
        query = f'''
        INSERT INTO {self._db_table} (user_id, token, expires_at) VALUES ($1, $2, $3)
        '''
        await self._con.execute(query, data.user_id, data.token, data.expires_at)
        
    async def update(self, data: dto.RefreshToken.Update.Input) -> None:
        query = f'''
        UPDATE {self._db_table} SET token=$2, expires_at=$3 WHERE token=$1;
        '''
        await self._con.execute(query, data.token, data.new_token, data.new_expires_at)
        
    async def delete(self, data: dto.RefreshToken.Delete.Input) -> None:
        query = f'''
        DELETE FROM {self._db_table} WHERE token=$1;
        '''
        await self._con.execute(query, data.token)
        
    async def verify(self, data: dto.RefreshToken.Verify.Input) -> bool:
        query = f'''
        SELECT EXISTS (SELECT 1 FROM {self._db_table} WHERE user_id=$1 AND token=$2 AND expires_at>=NOW());
        '''
        return await self._con.fetchval(query, data.user_id, data.token)
