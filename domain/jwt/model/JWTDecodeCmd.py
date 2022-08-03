from domain.util.dto_utils import to_string


class JWTDecodeCmd:
    def __init__(self, jwt: str):
        self.jwt = jwt

    def __str__(self):
        return to_string(self)
