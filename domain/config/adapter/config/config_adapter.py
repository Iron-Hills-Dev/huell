import logging

from flask import Config

from domain.config.config_port import ConfigPort
from domain.config.model.JWTConfig import JWTConfig
from domain.config.model.UserConfig import UserConfig

USER_CONFIG_PREFIX = "HUELL_USER_"
JWT_CONFIG_PREFIX = "HUELL_JWT_"


class ConfigAdapter(ConfigPort):
    def __init__(self, config: Config):
        self.config = config

    def read_user_config(self) -> UserConfig:
        logging.debug(f"Reading user config")
        _config = UserConfig(
            self.config.get(f"{USER_CONFIG_PREFIX}USERNAME_CHAR_WL"),
            self.config.get(f"{USER_CONFIG_PREFIX}USERNAME_CHAR_BL"),
            self.config.get(f"{USER_CONFIG_PREFIX}USERNAME_MIN_LEN"),
            self.config.get(f"{USER_CONFIG_PREFIX}USERNAME_MAX_LEN"),
            self.config.get(f"{USER_CONFIG_PREFIX}PASSWD_CHAR_WL"),
            self.config.get(f"{USER_CONFIG_PREFIX}PASSWD_CHAR_BL"),
            self.config.get(f"{USER_CONFIG_PREFIX}PASSWD_MIN_LEN"),
            self.config.get(f"{USER_CONFIG_PREFIX}PASSWD_MAX_LEN")
        )
        logging.debug(f"Read user config: {_config}")
        return _config

    def read_jwt_config(self) -> JWTConfig:
        try:
            logging.debug(f"Reading JWT config")
            _config = JWTConfig(
                self.config.get(f"{JWT_CONFIG_PREFIX}SECRET"),
                self.config.get(f"{JWT_CONFIG_PREFIX}ALGORITHM"),
                self.config.get(f"{JWT_CONFIG_PREFIX}EXP_TIME")
            )
            logging.debug(f"Read JWT config: {_config}")
            return _config
        except KeyError as e:
            logging.critical(f"ABORTING INIT - unknown {e.args[0]} environment variable")
            exit(1)
