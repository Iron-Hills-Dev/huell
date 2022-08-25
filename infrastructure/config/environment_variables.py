import logging
from os import environ

from flask import Config

ENV_PREFIX = "HUELL_"
USER_CONFIG_PREFIX = "USER_"
JWT_CONFIG_PREFIX = "JWT_"

default_envs = {
    f"{ENV_PREFIX}{USER_CONFIG_PREFIX}USERNAME_CHAR_WL": "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890.:_-+=",
    f"{ENV_PREFIX}{USER_CONFIG_PREFIX}USERNAME_CHAR_BL": "",
    f"{ENV_PREFIX}{USER_CONFIG_PREFIX}USERNAME_MIN_LEN": 4,
    f"{ENV_PREFIX}{USER_CONFIG_PREFIX}USERNAME_MAX_LEN": 16,
    f"{ENV_PREFIX}{USER_CONFIG_PREFIX}PASSWD_CHAR_WL": "",
    f"{ENV_PREFIX}{USER_CONFIG_PREFIX}PASSWD_CHAR_BL": "",
    f"{ENV_PREFIX}{USER_CONFIG_PREFIX}PASSWD_MIN_LEN": 7,
    f"{ENV_PREFIX}{USER_CONFIG_PREFIX}PASSWD_MAX_LEN": 25,
    f"{ENV_PREFIX}{JWT_CONFIG_PREFIX}ALGORITHM": "HS512",
    f"{ENV_PREFIX}{JWT_CONFIG_PREFIX}EXP_TIME": 1800,
    f"{ENV_PREFIX}LOGLEVEL": "INFO",
    f"{ENV_PREFIX}PERSISTENT_PORT": "DATABASE",
    f"{ENV_PREFIX}JWT_PORT": "JWT",
    f"{ENV_PREFIX}CONFIG_PORT": "CONFIG",
}


def import_envs(config: Config):
    """
    Imports all environment variables to app config
    :param config: app's config
    """
    logging.info("Importing environment variables")
    for k, v in environ.items():
        if k.startswith(ENV_PREFIX):
            config.update({k: v})
            logging.debug(f"Environment variable has been imported: {k}")

    for k in default_envs:
        if config.get(k) is None:
            config.update({k: default_envs[k]})

    logging.info("Environment variables imported successfully")
