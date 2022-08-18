from flask import Flask

from application.exceptions import BadRequest, MethodNotAllowed
from application.util.exception_utils import handle_exception
from infrastructure.config.environment_variables import import_envs
from infrastructure.config.ports import AppPorts
from infrastructure.logging.logging_init import logging_init

_app_ = Flask(__name__)

import_envs(_app_.config)
logging_init(_app_.config)
_ports_ = AppPorts(_app_.config)


@_app_.errorhandler(400)
def bad_request(error):
    return handle_exception(BadRequest("The browser (or proxy) sent a request that this server could not understand."))


@_app_.errorhandler(405)
def bad_request(error):
    return handle_exception(MethodNotAllowed("The method is not allowed for the requested URL."))


from application.user import user_rest_adapter
from application.auth import auth_rest_adapter
