import logging

from flask import Config

from domain.config.adapter.config.config_adapter import ConfigAdapter
from domain.config.config_port import ConfigPort
from domain.jwt.adapter.jwt.jwt_adapter import JWTAdapter
from domain.jwt.jwt_port import JWTPort
from domain.user.user_modify_port import UserModifyPort
from domain.user.user_query_port import UserQueryPort
import infrastructure.util.fake_adapters.fake_adapters as fake
from infrastructure.postgres.init_db import init_database
from infrastructure.postgres.user.database_user_modify_adapter import DatabaseUserModifyAdapter
from infrastructure.postgres.user.database_user_query_adapter import DatabaseUserQueryAdapter


class AppPorts:
    def __init__(self, _config: Config) -> None:
        self.config_port = config_config_module(_config)
        self.user_modify_port, self.user_query_port = config_user_module(_config, self.config_port)
        self.jwt_port = config_jwt_module(_config, self.config_port)


def config_user_module(_config: Config, _config_port: ConfigPort) -> tuple[UserModifyPort, UserQueryPort]:
    """
    Configures user module
    :param _config: App config (environments)
    :param _config_port: Config port (from config module)
    :return: Chosen user adapter
    """
    logging.info("Configuring user ports")
    match _config.get("HUELL_PERSISTENT_PORT"):
        case "DATABASE":
            logging.info("Chosen user ports configuration: DATABASE")
            _engine_ = init_database(_config)
            _user_config = _config_port.read_user_config()
            return DatabaseUserModifyAdapter(_engine_, _user_config), DatabaseUserQueryAdapter(_engine_)
        case "TEST":
            logging.warning("Chosen user ports configuration: TEST - will not work")
            return fake.FakeUserModifyAdapter(), fake.FakeUserQueryAdapter()
        case _:
            logging.critical("ABORTING INIT - unknown HUELL_PERSISTENT_PORT environment variable")
            exit(1)


def config_config_module(_config: Config) -> ConfigPort:
    """
    Configures config module
    :param _config: App config (environments)
    :return: Chosen config adapter
    """
    logging.info("Configuring config ports")
    match _config.get("HUELL_CONFIG_PORT"):
        case "CONFIG":
            logging.info("Chosen config ports configuration: YAML")
            return ConfigAdapter(_config)
        case "TEST":
            logging.warning("Chosen config ports configuration: TEST - will not work")
            return fake.FakeConfigAdapter()
        case _:
            logging.critical("ABORTING INIT - unknown HUELL_CONFIG_PORT environment variable")
            exit(1)


def config_jwt_module(_config: Config, _config_port: ConfigPort) -> JWTPort:
    """
    Configures JWT module
    :param _config: App config (environments)
    :param _config_port: Config port (from config module)
    :return: Chosen JWT adapter
    """
    logging.info("Configuring JWT ports")
    match _config.get("HUELL_JWT_PORT"):
        case "JWT":
            logging.info("Chosen JWT ports configuration: JWT")
            _jwt_config = _config_port.read_jwt_config()
            return JWTAdapter(_jwt_config)
        case "TEST":
            logging.warning("Chosen JWT ports configuration: TEST - will not work")
            return fake.FakeJWTAdapter()
        case _:
            logging.critical("ABORTING INIT - unknown HUELL_JWT_PORT environment variable")
            exit(1)
