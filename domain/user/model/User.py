from uuid import UUID

from domain.util.dto_utils import to_string

_SENSITIVE_FIELDS = ["password"]


class User:
    def __init__(self, _id: UUID, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return to_string(self, _SENSITIVE_FIELDS)
