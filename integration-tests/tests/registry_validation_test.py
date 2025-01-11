import allure
import pytest

from main import RegistryApiBuilder, PublicApi, DbActions, UserDbBuilder
from main.utils import CustomFaker, Role

fake = CustomFaker()

class TestRegistryValidation:

    @pytest.mark.asyncio
    async def test_should_registry_success(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить валидное тело запроса registry"):
            user: dict = RegistryApiBuilder().build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step("Проверить, что ответ - 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что в БД сохранен user с валидными параметрами"):
            result = await db_actions.get_user_by_login(user['login'])

            assert result is not None

            assert result['Login'] == user['login']
            assert result['UserId'] is not None
            assert result['Name'] == user['name']
            assert result['Role'] == user['role']
            assert result['PasswordHash'] is not None


    @pytest.mark.asyncio
    async def test_should_return_user_already_exist(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить для БД валидную строку user"):
            user_record: dict = UserDbBuilder().build()

        with allure.step("Заинжектить user в БД"):
            await db_actions.insert_user(user_record)

        with allure.step("Подготовить валидное тело запроса registry с уже использованным логином"):
            user: dict = RegistryApiBuilder().set_login(user_record['login']).build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step("Проверить, что ответ - 409 UserAlreadyExist"):
            assert response.status_code == 409
            assert response.json()['code'] == "UserAlreadyExist"


    @pytest.mark.asyncio
    async def test_should_return_invalid_email_format(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить тело запроса registry c невалидным форматом email"):
            invalid_email = 'invalid_format'
            user: dict = RegistryApiBuilder().set_login(invalid_email).build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step("Проверить, что ответ - 400 InvalidEmailFormat"):
            assert response.status_code == 400
            assert response.json()['code'] == "InvalidEmailFormat"


    @pytest.mark.asyncio
    async def test_should_return_password_too_short(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить тело запроса registry с паролем менее 8 символов"):
            short_password = fake.password(length=7)
            user: dict = RegistryApiBuilder().set_password(short_password).build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step("Проверить, что ответ - 400 PasswordTooShort"):
            assert response.status_code == 400
            assert response.json()['code'] == "PasswordTooShort"


    @pytest.mark.asyncio
    async def test_should_return_password_missing_uppercase(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить тело запроса registry с паролем не содержащим uppercase"):
            invalid_password = fake.password(upper_case=False)
            user: dict = RegistryApiBuilder().set_password(invalid_password).build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step("Проверить, что ответ - 400 PasswordMissingUppercase"):
            assert response.status_code == 400
            assert response.json()['code'] == "PasswordMissingUppercase"


    @pytest.mark.asyncio
    async def test_should_return_password_missing_special_characters(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить тело запроса registry с паролем не содержащим special characters"):
            invalid_password = fake.password(special_chars=False)
            user: dict = RegistryApiBuilder().set_password(invalid_password).build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step("Проверить, что ответ - 400 PasswordMissingSpecialCharacter"):
            assert response.status_code == 400
            assert response.json()['code'] == "PasswordMissingSpecialCharacter"


    @pytest.mark.asyncio
    async def test_should_return_password_missing_digits(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step("Подготовить тело запроса registry с паролем не содержащим digits"):
            invalid_password = fake.password(digits=False)
            user: dict = RegistryApiBuilder().set_password(invalid_password).build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step("Проверить, что ответ - 400 PasswordMissingDigit"):
            assert response.status_code == 400
            assert response.json()['code'] == "PasswordMissingDigit"


    @pytest.mark.parametrize(
        "input_value, expected_status",
        [
            (Role.client, 200),
            (Role.renter, 200),
        ]
    )
    @pytest.mark.asyncio
    async def test_should_accept_valid_role(self, public_api: PublicApi, db_actions: DbActions, input_value, expected_status):
        with allure.step(f"Подготовить тело запроса registry с ролью {input_value}"):
            user: dict = RegistryApiBuilder().set_role(input_value).build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step(f"Проверить, что ответ - {expected_status}"):
            assert response.status_code == expected_status

    @pytest.mark.asyncio
    async def test_should_fail_for_invalid_role(self, public_api: PublicApi, db_actions: DbActions):
        with allure.step(f"Подготовить тело запроса registry с не существующей ролью"):
            invalid_role = "invalid_role"
            user: dict = RegistryApiBuilder().set_role(invalid_role).build()

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step(f"Проверить, что ответ - 400 InvalidRole"):
            assert response.status_code == 400
            assert response.json()['code'] == "InvalidRole"


    @pytest.mark.parametrize(
        "login, name, password, role",
        [
            (None, fake.name(), fake.valid_password(), Role.client),
            (fake.email(), None, fake.valid_password(), Role.client),
            (fake.email(), fake.name(), None, Role.client)
        ]
    )
    @pytest.mark.asyncio
    async def test_should_return_fail_for_empty_fields(self, public_api: PublicApi, db_actions: DbActions, login, name,
                                                           password, role):
        with allure.step(
                f"Подготовить тело запроса registry с login: {login}, name: {name}, password: {password}, role: {role}"):
            user: dict = (
                RegistryApiBuilder()
                .set_login(login)
                .set_name(name)
                .set_password(password)
                .set_role(role)
                .build()
            )

        with allure.step("Отправить запрос регистрации пользователя"):
            response = await public_api.registry_user(user)

        with allure.step(f"Проверить, что ответ - 400 UnexpectedError"):
            assert response.status_code == 400
            assert response.json()['code'] == "UnexpectedError"
