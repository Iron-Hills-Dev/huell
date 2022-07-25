_EXCEPTION_PREFIX_ = "JWT-"


class JWTDecodeError(Exception):
    def __init__(self, _desc: str):
        self.desc = _desc
        self.html_code = 406
        self.code = f"{_EXCEPTION_PREFIX_}DE"
