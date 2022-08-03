from application.util.variable_type_check import is_instance
from domain.util.dto_utils import to_string


class UserCreateRequest:
    def __init__(self, username: str, password: str):
        is_instance(username, str, "username")
        is_instance(password, str, "password")
        self.username = username
        self.password = password

    def __str__(self):
        return to_string(self, ["password"])
