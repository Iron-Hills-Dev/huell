import logging

from flask import request

from app import _app_
from app import _ports_
from application.exceptions import InvalidVariableType
from application.user.model.UserCreateRequest import UserCreateRequest
from application.user.model.UserCreateResponse import UserCreateResponse
from application.util.exception_utils import exception_handler
from application.util.headers_check import headers_check
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError, UserCreateError
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.user_modify_port import UserModifyPort

modify: UserModifyPort = _ports_.user_modify_port


@_app_.route(f"/user", methods=["POST"])
@headers_check({"Accept": "application/json", "Content-Type": "application/json"})
def create_user():
    try:
        logging.info(f"Processing create user request: {request}")
        body_json = request.get_json()
        body = UserCreateRequest(body_json["username"], body_json["password"])
        logging.debug(f"Request body: {body}")
        cmd = UserCreateCmd(body.username, body.password)
        user_id = modify.create_user(cmd)
        response = UserCreateResponse(user_id)
        logging.info(f"Request processed successfully: {response}")
        return response.to_dict(), 201
    except (InvalidVariableType, UsernameSyntaxError, PasswordSyntaxError, UserCreateError) as e:
        return exception_handler(e)
