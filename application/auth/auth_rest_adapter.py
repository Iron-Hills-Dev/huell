import logging
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import request

from app import _app_, _ports_
from application.auth.exceptions import AuthError
from application.auth.model.UserLoginRequest import UserLoginRequest
from application.auth.model.UserLoginResponse import UserLoginResponse
from application.util.exception_utils import handle_exception
from application.util.headers_check import headers_check
from domain.jwt.jwt_port import JWTPort
from domain.jwt.model.JWTSignCmd import JWTSignCmd
from domain.user.exceptions import UserNotFound
from domain.user.user_query_port import UserQueryPort

AUTH_ERR_DESC = "Incorrect username or password"

jwt: JWTPort = _ports_.jwt_port
user_query: UserQueryPort = _ports_.user_query_port
ph = PasswordHasher()


@_app_.route("/login", methods=["POST"])
@headers_check({"Accept": "application/json", "Content-Type": "application/json"})
def login():
    try:
        logging.info(f"Processing login request: {request}")
        body = parse_login_request_body()
        user = user_query.find_user_by_username(body.username)
        ph.verify(user.password, body.password)
        token = create_token(user.id)
        response = UserLoginResponse(token)
        logging.info(f"Login request processed successfully")
        return response.to_json(), 200
    except VerifyMismatchError:
        logging.error("Incorrect password")
        return handle_exception(AuthError(AUTH_ERR_DESC))
    except UserNotFound:
        return handle_exception(AuthError(AUTH_ERR_DESC))


def parse_login_request_body() -> UserLoginRequest:
    body = request.get_json()
    body = UserLoginRequest(body["username"], body["password"])
    logging.debug(f"Request content: {body}")
    return body


def create_token(user_id: UUID) -> str:
    cmd = JWTSignCmd(user_id)
    return jwt.sign(cmd)
