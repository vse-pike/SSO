import bcrypt
from faker import Faker


class Role:
    client = "client"
    renter = "renter"


class CustomFaker(Faker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def valid_password(
            self,
            length: int = 8,
            special_chars: bool = True,
            digits: bool = True,
            upper_case: bool = True,
            lower_case: bool = True,
    ) -> str:
        return self.password(
            length=length,
            special_chars=special_chars,
            digits=digits,
            upper_case=upper_case,
            lower_case=lower_case,
        )


def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием алгоритма BCrypt.
    """
    salt = bcrypt.gensalt(rounds=10, prefix=b"2a")
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
