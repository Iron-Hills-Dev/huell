import logging

from flask import Config

from domain.config.adapter.YAML.yaml_config_adapter import YAMLConfigAdapter
from domain.config.config_port import ConfigPort
from domain.user.adapter.database.database_user_modify_adapter import DatabaseUserModifyAdapter
from domain.user.adapter.database.database_user_query_adapter import DatabaseUserQueryAdapter
from domain.user.user_modify_port import UserModifyPort
from domain.user.user_query_port import UserQueryPort
from infrastructure.postgres.init_db import init_database


class AppPorts:
    def __init__(self, _config: Config) -> None:
        self.config_port = config_config_module(_config)
        self.user_modify_port, self.user_query_port = config_user_module(_config, self.config_port)


def config_user_module(_config: Config, _config_port: ConfigPort) -> [UserModifyPort, UserQueryPort]:
    """
        Prepares configuration of ports in USER module
    """
    logging.info("Configuring user ports")
    match _config.get("HUELL_USER_PORT"):
        case "DATABASE":
            logging.info("Configuring DATABASE user ports")
            _engine_ = init_database(_config)

            _query = DatabaseUserQueryAdapter(_engine_)
            _user_config = _config_port.read_user_config(_config.get("HUELL_CONFIG_PATH"))
            return DatabaseUserModifyAdapter(_engine_, _user_config, _query), _query
        case "TEST":
            logging.warning("TEST user ports - not working ports chosen")
            return UserModifyPort, UserQueryPort
        case _:
            logging.critical("ABORTING INIT - unknown HUELL_USER_PORT environment variable")
            exit(1)


def config_config_module(_config: Config) -> [ConfigPort]:
    logging.info("Configuring config ports")
    match _config.get("HUELL_CONFIG_PORT"):
        case "YAML":
            logging.info("Configuring YAML config ports")
            return YAMLConfigAdapter()
        case "TEST":
            logging.warning("TEST config ports - not working ports chosen")
            return ConfigPort
        case _:
            logging.critical("ABORTING INIT - unknown HUELL_CONFIG_PORT environment variable")
            exit(1)
