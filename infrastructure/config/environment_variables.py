import logging
from os import environ

from flask import Config

ENV_PREFIX = "HUELL_"


def import_envs(_config: Config):
    logging.info("Importing environment variables")
    for k, v in environ.items():
        if k.startswith(ENV_PREFIX):
            _config.update({k: v})
            logging.debug(f"Environment variable {k} has been imported")
    logging.info("Environment variables imported successfully")
