from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy import text


class RefsLoader:
    def __init__(self, conn: AsyncConnection) -> None:
        self._conn = conn
        
    async def load(self, path: str):
        with open(path, 'r') as f:
            sql_queries = f.read()
        
        raw_conn = await self._conn.get_raw_connection()
        await raw_conn.dbapi_connection.driver_connection.execute(sql_queries)
