from application.util.variable_type_check import is_instance
from domain.util.dto_utils import to_string


class UserCreateRequest:
    def __init__(self, request: dict):
        self.username = request["username"]
        self.password = request["password"]
        is_instance(self.username, str, "username")
        is_instance(self.password, str, "password")

    def __str__(self):
        return to_string(self, ["password"])

    def to_json(self):
        return self.__dict__
