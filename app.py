from flask import Flask

from infrastructure.config.environment_variables import import_envs
from infrastructure.logging.logging_init import logging_init

_app_ = Flask(__name__)

import_envs(_app_.config)
logging_init(_app_.config)
