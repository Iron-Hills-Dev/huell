import logging

import sqlalchemy
from flask import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from infrastructure.postgres.model.user_entity import UserEntity
from infrastructure.postgres.model.version_entity import VersionEntity

_version_ = "1.0"


def init_database(_config: Config) -> Engine:
    logging.info("Initializing database")
    _engine_ = get_db_engine(_config["HUELL_DB_URL"])
    logging.debug("Checking if database strcuture exists")
    if not sqlalchemy.inspect(_engine_).has_table("version"):
        logging.warning("Database structure does not exist")
        create_database_structure(_engine_)
    else:
        if is_structure_outdated(_engine_):
            logging.critical("ABORTING INIT - Database structure is outdated")
            exit(1)
    logging.info("Database initialized successfully")
    return _engine_


def create_database_structure(_engine_: Engine) -> None:
    logging.info("Creating database structure")
    create_version_ref(_engine_)
    create_user_table(_engine_)
    logging.info("Created database structure successfully")


def get_db_engine(_url: str) -> Engine:
    logging.info("Initializing database engine")
    if not database_exists(_url):
        logging.warning(f"Database doesn't exist: creating")
        create_database(_url)

    logging.debug("Creating database engine")
    _engine_ = create_engine(_url)
    logging.info("Database engine initialized successfully")
    return _engine_


def create_version_ref(_engine_: Engine) -> None:
    logging.debug("Creating version table")
    version_tab = VersionEntity(version=_version_)
    version_tab.create(_engine_)
    with Session(_engine_) as session:
        logging.debug(f"Creating version reference (version: {_version_})")
        session.add(version_tab)
        session.commit()


def is_structure_outdated(_engine_: Engine) -> bool:
    logging.debug("Checking if db structure is outdated")
    with Session(_engine_) as session:
        _version = session.query(VersionEntity).first()
        if _version.version != _version_:
            logging.warning("Db structure is outdated!")
            return True
    logging.debug("Db structure is not outdated")
    return False


def create_user_table(_engine_: Engine) -> None:
    logging.debug("Creating user table")
    user_tab = UserEntity()
    user_tab.create(_engine_)
