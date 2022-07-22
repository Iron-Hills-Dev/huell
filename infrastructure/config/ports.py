import logging

from flask import Config

from domain.user.adapter.database.database_user_modify_adapter import DatabaseUserModifyAdapter
from domain.user.adapter.database.database_user_query_adapter import DatabaseUserQueryAdapter
from domain.user.user_modify_port import UserModifyPort
from domain.user.user_query_port import UserQueryPort
from infrastructure.postgres.init_db import init_database


class AppPorts:
    def __init__(self, _config: Config) -> None:
        self.user_modify_port, self.user_query_port = config_user_module(_config)


def config_user_module(_config: Config) -> [UserModifyPort, UserQueryPort]:
    """
        Prepares configuration of ports in USER module
    """
    logging.info("Configuring user ports")
    match _config.get("HUELL_USER_PORT"):
        case "DATABASE":
            logging.info("Configuring DATABASE user ports")
            _engine_ = init_database(_config)
            _query = DatabaseUserQueryAdapter(_engine_)
            return DatabaseUserModifyAdapter(_engine_, _query), _query
        case "TEST":
            logging.warning("TEST user ports - not working ports will be chosen")
            return UserModifyPort, UserQueryPort
        case _:
            logging.critical("ABORTING INIT - unknown HUELL_USER_PORT environment variable")
            exit(1)
