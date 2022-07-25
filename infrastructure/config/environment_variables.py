import logging
from os import environ

from flask import Config

ENV_PREFIX = "HUELL_"


def import_envs(_config: Config):
    """
    Imports all environment variables required for app to work
    :param _config: App config (place for envs)
    """
    logging.info("Importing environment variables")
    for k, v in environ.items():
        if k.startswith(ENV_PREFIX):
            _config.update({k: v})
            logging.debug(f"Environment variable has been imported: {k}")
    logging.info("Environment variables imported successfully")
