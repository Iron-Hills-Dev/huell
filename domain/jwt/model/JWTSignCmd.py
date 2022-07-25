from uuid import UUID

from domain.util.dto_utils import to_string


class JWTSignCmd:
    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def __str__(self):
        return to_string(self)