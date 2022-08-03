from flask import Flask

from application.exceptions import BadRequest
from application.util.exception_utils import exception_handler
from infrastructure.config.environment_variables import import_envs
from infrastructure.config.ports import AppPorts
from infrastructure.logging.logging_init import logging_init

_app_ = Flask(__name__)

import_envs(_app_.config)
logging_init(_app_.config)
_ports_ = AppPorts(_app_.config)


@_app_.errorhandler(400)
def bad_request():
    return exception_handler(BadRequest("The browser (or proxy) sent a request that this server could not understand."))


from application.user import user_rest_adapter
