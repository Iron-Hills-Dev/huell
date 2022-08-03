from uuid import UUID

from domain.util.dto_utils import to_string


class UserCreateResponse:
    def __init__(self, _id: UUID):
        self.user_id = _id

    def __str__(self):
        return to_string(self)

    def to_dict(self):
        return {"userID": str(self.user_id)}
