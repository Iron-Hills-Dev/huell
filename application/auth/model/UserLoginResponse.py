from application.util.variable_type_check import is_instance


class UserLoginResponse:
    def __init__(self, token: str):
        is_instance(token, str, "token")
        self.token = token

    def to_json(self):
        return self.__dict__
