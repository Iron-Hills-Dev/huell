from application.util.variable_type_check import is_instance
from domain.util.dto_utils import to_string


class UserLoginResponse:
    def __init__(self, token: str):
        is_instance(token, str, "token")
        self.token = token

    def to_json(self):
        return self.__dict__

    def __str__(self):
        return to_string(self)
