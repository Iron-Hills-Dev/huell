class JWTConfig:
    def __init__(self, algorithm: str, exp_time: int):
        self.algorithm = algorithm
        self.exp_time = exp_time