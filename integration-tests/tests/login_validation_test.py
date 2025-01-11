from datetime import datetime, timedelta, timezone

import allure
import pytest

from main import PublicApi, DbActions, UserDbBuilder, LoginApiBuilder
from main.utils import CustomFaker, hash_password

fake = CustomFaker()

@pytest.mark.regression
class TestLoginValidation:

    @pytest.mark.asyncio
    async def test_should_login_success(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить для БД валидную строку user"):
            password = fake.valid_password()
            password_hash = hash_password(password)

            user_record: dict = (
                UserDbBuilder()
                .set_password_hash(password_hash)
                .build()
            )

        with allure.step("Заинжектить user в БД"):
            await db_actions.insert_user(user_record)

        with allure.step("Подготовить валидное тело запроса login"):
            login: dict = (
                LoginApiBuilder()
                .set_login(user_record["login"])
                .set_password(password)
                .build()
            )

        with allure.step("Отправить запрос авторизации пользователя"):
            response = await public_api.login_user(login)

        with allure.step("Проверить, что ответ - 200"):
            assert response.status_code == 200
            token = response.json()["accessToken"]

        with allure.step("Проверить, что для user был создан актуальный токен"):
            token_record: dict = await db_actions.get_token_by_user_id(user_record["user_id"])

            assert token_record["UserId"] == user_record["user_id"]
            assert token_record["Token"] == token
            assert token_record["ExpirationDateTime"] is not None

    @pytest.mark.asyncio
    async def test_should_return_date_time_offset(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить для БД валидную строку user"):
            password = fake.valid_password()
            password_hash = hash_password(password)

            user_record: dict = (
                UserDbBuilder()
                .set_password_hash(password_hash)
                .build()
            )

        with allure.step("Заинжектить user в БД"):
            await db_actions.insert_user(user_record)

        with allure.step("Подготовить валидное тело запроса login"):
            login: dict = (
                LoginApiBuilder()
                .set_login(user_record["login"])
                .set_password(password)
                .build()
            )

        current_date_time = datetime.now(timezone.utc)

        with allure.step("Отправить запрос авторизации пользователя"):
            response = await public_api.login_user(login)

        with allure.step("Проверить, что ответ - 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что ExpirationDateTime установлен на 15 мин от текущего времени"):
            token_record: dict = await db_actions.get_token_by_user_id(user_record["user_id"])

            expiration_date_time = token_record["ExpirationDateTime"]

            if expiration_date_time.tzinfo is None:
                expiration_date_time = expiration_date_time.replace(tzinfo=timezone.utc)

            expected_expiration_time = current_date_time + timedelta(minutes=15)

            assert abs((expiration_date_time - expected_expiration_time).total_seconds()) <= 60

    @pytest.mark.asyncio
    async def test_should_fail_with_incorrect_login(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить для БД валидную строку user"):
            password = fake.valid_password()
            password_hash = hash_password(password)

            user_record: dict = (
                UserDbBuilder()
                .set_password_hash(password_hash)
                .build()
            )

        with allure.step("Заинжектить user в БД"):
            await db_actions.insert_user(user_record)

        with allure.step("Подготовить тело запроса с невалидным логином"):
            invalid_login = fake.email()

            login: dict = (
                LoginApiBuilder()
                .set_login(invalid_login)
                .set_password(password)
                .build()
            )

        with allure.step("Отправить запрос авторизации пользователя"):
            response = await public_api.login_user(login)

        with allure.step("Проверить, что ответ - 400 InvalidCredentials"):
            assert response.status_code == 400

            assert response.json()["code"] == "InvalidCredentials"

    @pytest.mark.asyncio
    async def test_should_fail_with_incorrect_password(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить для БД валидную строку user"):
            password = fake.valid_password()
            password_hash = hash_password(password)

            user_record: dict = (
                UserDbBuilder()
                .set_password_hash(password_hash)
                .build()
            )

        with allure.step("Заинжектить user в БД"):
            await db_actions.insert_user(user_record)

        with allure.step("Подготовить тело запроса с невалидным паролем"):
            invalid_password = fake.valid_password()

            login: dict = (
                LoginApiBuilder()
                .set_login(invalid_password)
                .set_password(password)
                .build()
            )

        with allure.step("Отправить запрос авторизации пользователя"):
            response = await public_api.login_user(login)

        with allure.step("Проверить, что ответ - 400 InvalidCredentials"):
            assert response.status_code == 400

            assert response.json()["code"] == "InvalidCredentials"

    @pytest.mark.parametrize("login, password", [
        (None, "password"),
        ("login", None)
    ])
    @pytest.mark.asyncio
    async def test_should_fail_with_incorrect_pair(self, public_api: PublicApi, db_actions: DbActions, login,
                                                   password):
        with allure.step("Подготовить тело запроса с невалидными данными - {login, password}"):
            login: dict = (
                LoginApiBuilder()
                .set_login(login)
                .set_password(password)
                .build()
            )

        with allure.step("Отправить запрос авторизации пользователя"):
            response = await public_api.login_user(login)

        with allure.step("Проверить, что ответ - 400 ModelException"):
            assert response.status_code == 400

            assert response.json()["code"] == "ModelException"

    @pytest.mark.asyncio
    async def test_should_update_token_with_second_request(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить для БД валидную строку user"):
            password = fake.valid_password()
            password_hash = hash_password(password)

            user_record: dict = (
                UserDbBuilder()
                .set_password_hash(password_hash)
                .build()
            )

        with allure.step("Заинжектить user в БД"):
            await db_actions.insert_user(user_record)

        with allure.step("Подготовить валидное тело запроса login"):
            login: dict = (
                LoginApiBuilder()
                .set_login(user_record["login"])
                .set_password(password)
                .build()
            )

        with allure.step("Отправить запрос авторизации пользователя"):
            response = await public_api.login_user(login)

        with allure.step("Проверить, что ответ - 200"):
            assert response.status_code == 200

        with allure.step("Получить актуальный токен из БД"):
            token_record_1: dict = await db_actions.get_token_by_user_id(user_record["user_id"])
            token_1 = token_record_1["Token"]
            date_time_1 = token_record_1["ExpirationDateTime"]

        with allure.step("Отправить запрос авторизации пользователя повторно"):
            response = await public_api.login_user(login)

        with allure.step("Проверить, что ответ - 200"):
            assert response.status_code == 200

        with allure.step("Получить актуальный токен из БД"):
            token_record_2: dict = await db_actions.get_token_by_user_id(user_record["user_id"])
            token_2 = token_record_2["Token"]
            date_time_2 = token_record_2["ExpirationDateTime"]

        with allure.step("Проверить, что значение token и expiration_date_time обновились после второго запроса"):
            assert token_1 != token_2
            assert date_time_1 != date_time_2
