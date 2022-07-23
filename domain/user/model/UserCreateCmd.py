from domain.util.dto_utils import to_string

_SENSITIVE_FIELDS = ["password"]


class UserCreateCmd:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return to_string(self, _SENSITIVE_FIELDS)
