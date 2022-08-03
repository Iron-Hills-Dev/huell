import logging


def exception_handler(exc) -> tuple:
    return {"code": exc.code, "desc": exc.desc}, exc.html_code
