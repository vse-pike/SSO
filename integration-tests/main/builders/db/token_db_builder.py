import uuid

from faker import Faker


class TokenDbBuilder:
    def __init__(self):
        fake = Faker()
        self.__user_id = str(uuid.uuid4())
        self.__token = str(uuid.uuid4())
        self.__expiration_date_time = fake.past_date()

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_token(self, token):
        self.__token = token

    def set_expiration_date_time(self, expiration_date_time):
        self.__expiration_date_time = expiration_date_time

    def build(self):
        return {
            'user_id': self.__user_id,
            'token': self.__token,
            'expiration_date_time': self.__expiration_date_time
        }
