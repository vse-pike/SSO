import allure
import httpx


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    @allure.step("Отправить запрос: POST {path}, data - {data}")
    async def post(self, path, data):
        return await self.client.post(url = path, json=data)

    @allure.step("Отправить запрос: GET {path}")
    async def get(self, path):
        return await self.client.get(url = path)

    @allure.step("Отправить запрос: DELETE {path}")
    async def delete(self, path):
        return await self.client.delete(url = path)

    @allure.step("Отправить запрос: PUT {path}, data - {data}")
    async def put(self, path, data):
        return await self.client.put(url = path, json = data)