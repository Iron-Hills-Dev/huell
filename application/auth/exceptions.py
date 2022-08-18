_EXCEPTION_PREFIX_ = "AUTH."


class AuthError(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 401
        self.code = f"{_EXCEPTION_PREFIX_}AE"
