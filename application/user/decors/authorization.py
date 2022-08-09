import logging
from functools import wraps

from flask import request

from application.user.exceptions import AuthorizationHeaderError
from application.util.exception_utils import handle_exception
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.jwt_port import JWTPort
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd


def authorization(jwt: JWTPort):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                header = request.headers["Authorization"]
                logging.debug(f"Authorizing user: header={header}")
                token = extract_token(header)
                payload = jwt.decode(JWTDecodeCmd(token))
                logging.debug(f"Authorized user: id={payload.user_id}")
                return f(payload.user_id, *args, **kwargs)
            except (JWTDecodeError, AuthorizationHeaderError) as e:
                return handle_exception(e)
            except KeyError as e:
                if e.args[0] != "HTTP_AUTHORIZATION":
                    raise e
                logging.error("Missing Authorization header")
                return handle_exception(AuthorizationHeaderError("Missing Authorization header"))

        return wrapper

    return decorator


def extract_token(header: str) -> str:
    if header.startswith("Bearer "):
        token = header[6:]
        logging.debug(f"Token extracted: token={token}")
        return token
    else:
        logging.error(f"Wrong Authorization header format: header={header}")
        raise AuthorizationHeaderError("Wrong Authorization header format (format accepted: Bearer `token`")
