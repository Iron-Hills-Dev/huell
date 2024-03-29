_EXCEPTION_PREFIX_ = "USER."


class UsernameSyntaxError(Exception):
    def __init__(self, _desc: str):
        self.desc = _desc
        self.html_code = 406
        self.code = f"{_EXCEPTION_PREFIX_}USE"


class PasswordSyntaxError(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 406
        self.code = f"{_EXCEPTION_PREFIX_}PSE"


class UserCreateError(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 503
        self.code = f"{_EXCEPTION_PREFIX_}UCE"


class UserDeleteError(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 503
        self.code = f"{_EXCEPTION_PREFIX_}UDE"


class ChangePasswordError(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 503
        self.code = f"{_EXCEPTION_PREFIX_}CPE"


class IncorrectPassword(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 406
        self.code = f"{_EXCEPTION_PREFIX_}IP"


class UserNotFound(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 404
        self.code = f"{_EXCEPTION_PREFIX_}UNF"


class UserFindError(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 503
        self.code = f"{_EXCEPTION_PREFIX_}UFE"
