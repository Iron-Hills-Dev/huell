_EXCEPTION_PREFIX_ = "JWT."


class JWTDecodeError(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 401
        self.code = f"{_EXCEPTION_PREFIX_}DE"
