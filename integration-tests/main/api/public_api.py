import allure

from main.api.http_client import HttpClient


class PublicApi:
    __registry_url = "/api/v1/registry"
    __login_url = "/api/v1/login"

    def __init__(self, client: HttpClient):
        self.__client = client

    @allure.step("Создать пользователя с data - {data}")
    async def registry_user(self, data):
        return await self.__client.post(path = self.__registry_url, data=data)

    @allure.step("Авторизовать пользователя с data - {data}")
    async def login_user(self, data):
        return await self.__client.post(path = self.__login_url, data=data)