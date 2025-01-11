import asyncpg


class DbClient:
    def __init__(self, dsn):
        self.__dsn = dsn
        self.__connection = None

    async def __aenter__(self):
        self.__connection = await asyncpg.connect(self.__dsn)
        return self.__connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__connection.close()

    async def execute(self, query, *args):
        try:
            return await self.__connection.execute(query, *args)
        except Exception as e:
            raise RuntimeError(f"Ошибка выполнения запроса: {query} с параметрами {args}") from e

    async def fetch(self, query, *args):
        try:
            return await self.__connection.fetch(query, *args)
        except Exception as e:
            raise RuntimeError(f"Ошибка выполнения запроса: {query} с параметрами {args}") from e