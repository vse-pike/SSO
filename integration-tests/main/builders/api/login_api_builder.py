from main.utils import CustomFaker


class LoginApiBuilder:
    def __init__(self):
        fake = CustomFaker()
        self.__login = fake.email()
        self.__password = fake.valid_password()

    def set_login(self, login):
        self.__login = login
        return self

    def set_password(self, password):
        self.__password = password
        return self

    def build(self):
        """Метод для возврата объекта в формате словаря JSON."""
        return {
            'login': self.__login,
            'password': self.__password
        }
