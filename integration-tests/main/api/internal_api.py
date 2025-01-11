import allure


class InternalApi:
    __access_url = "/api/v1/access"

    def __init__(self, client):
        self.__client = client

    @allure.step("Проверить access token с data - {data}")
    async def check_access_token(self, data):
        return await self.__client.post(path = self.__access_url, data=data)