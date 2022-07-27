from domain.util.dto_utils import to_string


class JWTConfig:
    def __init__(self, algorithm: str, exp_time: int, secret: str):
        self.algorithm = algorithm
        self.exp_time = exp_time
        self.secret = secret

    def __str__(self):
        return to_string(self, ["secret"])
