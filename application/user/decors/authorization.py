from functools import wraps

from flask import request

from application.user.exceptions import NoAuthorizationError
from application.util.exception_utils import exception_handler
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.jwt_port import JWTPort
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd


def authorization(jwt: JWTPort):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                _jwt = request.headers["Authorization"]
                payload = jwt.decode(JWTDecodeCmd(_jwt))
                return f(payload.user_id, *args, **kwargs)
            except JWTDecodeError as e:
                return exception_handler(e)
            except KeyError:
                return exception_handler(NoAuthorizationError("Missing authorization token"))

        return wrapper

    return decorator
