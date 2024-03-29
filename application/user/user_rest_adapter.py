import logging

from flask import request

from app import _app_
from app import _ports_
from application.exceptions import InvalidVariableType
from application.user.decors.authorization import authorization
from application.user.model.UserChangePasswordRequest import UserChangePasswordRequest
from application.user.model.UserCreateRequest import UserCreateRequest
from application.user.model.UserCreateResponse import UserCreateResponse
from application.user.model.UserFindResponse import UserFindResponse
from application.util.exception_utils import handle_exception
from application.util.headers_check import headers_check
from domain.jwt.jwt_port import JWTPort
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError, UserCreateError, UserNotFound, \
    UserDeleteError, ChangePasswordError, IncorrectPassword, UserFindError
from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
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
        return handle_exception(e)


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
    except (UserNotFound, UserFindError) as e:
        return handle_exception(e)


@_app_.route("/user", methods=["DELETE"])
@authorization(jwt)
@headers_check({"Accept": "*/*"})
def delete_user(user_id):
    try:
        logging.info(f"Processing delete user request: user_id={user_id}")
        cmd = UserDeleteCmd(user_id)
        modify.delete_user(cmd)
        logging.info("Request processed successfully")
        return "", 204
    except (UserNotFound, UserDeleteError) as e:
        return handle_exception(e)


@_app_.route("/user/change-passwd", methods=["PUT"])
@authorization(jwt)
@headers_check({"Accept": "*/*", "Content-Type": "application/json"})
def change_password(user_id):
    try:
        logging.info(f"Processing change user password request: user_id={user_id}")
        body = request.get_json()
        body = UserChangePasswordRequest(body["currentPassword"], body["newPassword"])
        cmd = ChangePasswordCmd(user_id, body.current_password, body.new_password)
        modify.change_password(cmd)
        logging.info("Request processed successfully")
        return "", 204
    except (UserNotFound, ChangePasswordError, IncorrectPassword, InvalidVariableType) as e:
        return handle_exception(e)
