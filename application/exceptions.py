_EXCEPTION_PREFIX_ = "APP."


class BadRequest(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 400
        self.code = f"{_EXCEPTION_PREFIX_}BR"


class MethodNotAllowed(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 405
        self.code = f"{_EXCEPTION_PREFIX_}MNA"


class InvalidVariableType(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 400
        self.code = f"{_EXCEPTION_PREFIX_}IVT"


class WrongHeaderError(Exception):
    def __init__(self, desc: str):
        self.desc = desc
        self.html_code = 400
        self.code = f"{_EXCEPTION_PREFIX_}WHE"
