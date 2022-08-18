from uuid import UUID

from domain.util.dto_utils import to_string


class UserFindResponse:
    def __init__(self, _id: UUID, username: str):
        self.username = username
        self.id = _id

    def to_json(self):
        return {"id": str(self.id), "username": self.username}

    def __str__(self):
        return to_string(self)
