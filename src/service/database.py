from abc import ABCMeta, abstractmethod
import typing as tp
import asyncpg


class IDatabase(metaclass=ABCMeta):

    @abstractmethod
    async def startup(self, dsn: str) -> None:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass

    @abstractmethod
    async def connection(self):
        pass


class ASPGDatabase(IDatabase):
    def __init__(self):
        self.pool: tp.Optional[asyncpg.Pool] = None

    async def startup(self, dsn: str) -> None:
        """
        Создание асинхронного пула подключений к бд.
        """
        self.pool = await asyncpg.create_pool(dsn, timeout=5)

    async def shutdown(self) -> None:
        """
        Закрытие пула подключений.
        """
        await self.pool.close()

    async def connection(self) -> asyncpg.Connection:
        """
        Получение подключения из пула.
        """
        if self.pool is None:
            raise NotImplementedError('DB pool must be created first')
        con = await self.pool.acquire()
        try:
            yield con
        finally:
            await self.pool.release(con)


database = ASPGDatabase()
