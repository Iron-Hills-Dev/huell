from uuid import UUID

from domain.util.dto_utils import to_string


class JWTPayload:
    def __init__(self, iss: str, sub: str, exp: int, iat: int, user_id: UUID):
        self.iss = iss
        self.sub = sub
        self.exp = exp
        self.iat = iat
        self.user_id = user_id

    def to_dict(self):
        _dict = self.__dict__.copy()
        _dict["user_id"] = str(self.user_id)
        return _dict

    def __str__(self):
        return to_string(self)
