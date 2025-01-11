import random
import uuid

from faker import Faker

from main.utils import Role


class UserDbBuilder:
    def __init__(self):
        fake = Faker()
        self.__user_id = str(uuid.uuid4())
        self.__name = fake.name()
        self.__login = fake.email()
        self.__password_hash = str(uuid.uuid4())
        self.__role = random.choice([Role.client, Role.renter])

    def set_user_id(self, user_id):
        self.__user_id = user_id
        return self

    def set_name(self, name):
        self.__name = name
        return self

    def set_login(self, login):
        self.__login = login
        return self

    def set_password_hash(self, password_hash):
        self.__password_hash = password_hash
        return self

    def set_role(self, role):
        self.__role = role
        return self

    def build(self):
        return {
            'user_id': self.__user_id,
            'name': self.__name,
            'login': self.__login,
            'password_hash': self.__password_hash,
            'role': self.__role
        }