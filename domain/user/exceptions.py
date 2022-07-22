class UsernameSyntaxError(Exception):
    def __init__(self, _desc: str):
        self.desc = _desc
        self.html_code = 406
        self.code = "USE"


class PasswordSyntaxError(Exception):
    def __init__(self, _desc: str):
        self.desc = _desc
        self.html_code = 406
        self.code = "PSE"


class AuthError(Exception):
    def __init__(self, _desc: str):
        self.desc = _desc
        self.html_code = 406
        self.code = "AE"


class UserNotFound(Exception):
    def __init__(self, _desc: str):
        self.desc = _desc
        self.html_code = 404
        self.code = "UNF"
