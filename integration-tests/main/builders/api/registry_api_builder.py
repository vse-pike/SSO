import random

from main.utils import Role, CustomFaker


class RegistryApiBuilder:
    def __init__(self):
        fake = CustomFaker()
        self.__login = fake.email()
        self.__password = fake.valid_password()
        self.__name = fake.name()
        self.__role = random.choice([Role.client, Role.renter])

    def set_login(self, login):
        self.__login = login
        return self

    def set_password(self, password):
        self.__password = password
        return self

    def set_name(self, name):
        self.__name = name
        return self

    def set_role(self, role):
        self.__role = role
        return self

    def build(self):
        """Метод для возврата объекта в формате словаря JSON."""
        return {
            'login': self.__login,
            'password': self.__password,
            'name': self.__name,
            'role': self.__role
        }
