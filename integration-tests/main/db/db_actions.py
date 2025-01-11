import allure

from .db_client import DbClient


class DbActions:
    """Использовать только внутри фикстуры db_actions, чтобы избежать проблемы с управлением содинения self.__client"""
    def __init__(self, db_client: DbClient):
        self.__client = db_client

    @allure.step("Добавить пользователя в БД с data - {data}")
    async def insert_user(self, data: dict[str, str]):
        await self.__client.execute(
            'INSERT INTO "Users" ("UserId", "Name", "Login", "PasswordHash", "Role") VALUES ($1, $2, $3, $4, $5)',
            data['user_id'], data['name'], data['login'], data['password_hash'], data['role'])

    @allure.step("Получить пользователя из БД по логину - {login}")
    async def get_user_by_login(self, login):
        result = await self.__client.fetch('SELECT * FROM "Users" WHERE "Login" = $1', login)
        if result:
            user = dict(result[0])
            return user
        else:
            return None

    @allure.step("Добавить токен в БД с data - {data}")
    async def insert_token(self, data: dict[str, str]):
        await self.__client.execute('INSERT INTO "Tokens" ("UserId", "Token", "ExpirationDateTime") VALUES ($1, $2, $3)',
                                    data['user_id'], data['token'], data['expiration_date_time'])

    @allure.step("Получить токен из БД")
    async def get_token_by_user_id(self, user_id):
        result = await self.__client.fetch('SELECT * FROM "Tokens" WHERE "UserId" = $1', user_id)
        if result:
            token = dict(result[0])
            return token
        else:
            return None

    async def truncate(self):
        """Использовать только из фикстуры локального запуска тестов"""
        await self.__client.execute('TRUNCATE TABLE "Users" CASCADE')
        await self.__client.execute('TRUNCATE TABLE "Tokens" CASCADE')
