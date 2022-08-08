import logging
from functools import wraps

from flask import request

from application.exceptions import WrongHeaderError
from application.util.exception_utils import exception_handler


def headers_check(valid_headers: dict):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            logging.debug("Checking headers")
            header = None
            headers = request.headers
            try:
                for header in valid_headers.keys():
                    logging.debug(f"Checking header: {header}")
                    if valid_headers[header] != headers[header]:
                        if valid_headers[header] is not None:
                            logging.error(f"Wrong header: {header}={headers[header]}")
                            return exception_handler(WrongHeaderError(
                                f"Wrong {header} header ({headers[header]} vs {valid_headers[header]})"))
                return f(*args, **kwargs)
            except KeyError:
                logging.error(f"Missing header: {header}")
                return exception_handler(WrongHeaderError(f"Missing header: {header}"))

        return wrapper

    return decorator
