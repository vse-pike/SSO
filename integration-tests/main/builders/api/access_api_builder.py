import uuid


class AccessApiBuilder:
    def __init__(self):
        self.__access_token = uuid.uuid4()

    def set_access_token(self, access_token):
        self.__access_token = access_token

    def build(self):
        """Метод для возврата объекта в формате словаря JSON."""
        return {
            'access_token': self.__access_token
        }
