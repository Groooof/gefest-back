import asyncpg
from uuid import UUID

from . import schemas as sch


class PostgresCandidatesRepo:
    _db_table = 'candidates'
    
    def __init__(self, con: asyncpg.Connection) -> None:
        self._con = con
        
    async def create(self, data: sch.Create.Request.Body, creator_id: UUID) -> dto.Candidates.Create.Output:
        query = f'''
        INSERT INTO {self._db_table}
        (
            post,
            first_name,
            last_name,
            middle_name,
            birth_date,
            min_salary,
            adress_code,
            citizenship_code,
            family_status_code,
            creator_id
        )
        ;
        '''
        res = await self._con.fetch(query)
        print(res)
        return dto.Roles.GetAll.Output(roles=[dto.RoleInfo(**row) for row in res])
