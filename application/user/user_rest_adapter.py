import logging

from flask import request

from app import _app_
from app import _ports_
from application.exceptions import InvalidVariableType
from application.user.decors.authorization import authorization
from application.user.model.UserCreateRequest import UserCreateRequest
from application.user.model.UserCreateResponse import UserCreateResponse
from application.user.model.UserFindResponse import UserFindResponse
from application.util.exception_utils import exception_handler
from application.util.headers_check import headers_check
from domain.jwt.jwt_port import JWTPort
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError, UserCreateError, UserNotFound, \
    UserDeleteError
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd
from domain.user.user_modify_port import UserModifyPort
from domain.user.user_query_port import UserQueryPort

modify: UserModifyPort = _ports_.user_modify_port
query: UserQueryPort = _ports_.user_query_port
jwt: JWTPort = _ports_.jwt_port


@_app_.route("/user", methods=["POST"])
@headers_check({"Accept": "application/json", "Content-Type": "application/json"})
def create_user():
    try:
        logging.info(f"Processing create user request: {request}")
        body = request.get_json()
        body = UserCreateRequest(body["username"], body["password"])
        logging.debug(f"Request body: {body}")
        cmd = UserCreateCmd(body.username, body.password)
        user_id = modify.create_user(cmd)
        response = UserCreateResponse(user_id)
        logging.info(f"Request processed successfully: {response}")
        return response.to_json(), 201
    except (InvalidVariableType, UsernameSyntaxError, PasswordSyntaxError, UserCreateError) as e:
        return exception_handler(e)


@_app_.route("/user", methods=["GET"])
@authorization(jwt)
@headers_check({"Accept": "application/json"})
def find_user(user_id):
    try:
        logging.info(f"Processing find user request: user_id={user_id}")
        user = query.find_user_by_id(user_id)
        response = UserFindResponse(user.id, user.username)
        logging.info(f"Request processed successfully: {response}")
        return response.to_json(), 200
    except UserNotFound as e:
        return exception_handler(e)


@_app_.route("/user", methods=["DELETE"])
@authorization(jwt)
@headers_check({"Accept": "text/plain"})
def delete_user(user_id):
    try:
        logging.info(f"Processing delete user request: user_id={user_id}")
        cmd = UserDeleteCmd(user_id)
        modify.delete_user(cmd)
        logging.info("Request processed successfully")
        return "", 204
    except (UserNotFound, UserDeleteError) as e:
        return exception_handler(e)