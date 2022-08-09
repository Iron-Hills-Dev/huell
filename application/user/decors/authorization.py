import logging
from functools import wraps

from flask import request

from application.user.exceptions import NoAuthorizationError
from application.util.exception_utils import handle_exception
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.jwt_port import JWTPort
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd


def authorization(jwt: JWTPort):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                _jwt = request.headers["Authorization"]
                logging.debug(f"Authorizing user: token={_jwt}")
                payload = jwt.decode(JWTDecodeCmd(_jwt))
                logging.debug(f"Authorized user: id={payload.user_id}")
                return f(payload.user_id, *args, **kwargs)
            except JWTDecodeError as e:
                return handle_exception(e)
            except KeyError as e:
                if e.args[0] != "HTTP_AUTHORIZATION":
                    raise e
                return handle_exception(NoAuthorizationError("Missing authorization token"))

        return wrapper

    return decorator
