import logging

import sqlalchemy
from flask import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from infrastructure.postgres.model.VersionEntity import VersionEntity
from infrastructure.postgres.model.dec_base import create_all_tables

VERSION = "1.0"


def init_database(config: Config) -> Engine:
    logging.info("Initializing database")
    engine = get_db_engine(config["HUELL_DB_URL"])
    logging.debug("Checking if database strcuture exists")
    if not sqlalchemy.inspect(engine).has_table("version"):
        logging.warning("Database structure does not exist")
        create_database_structure(engine)
    else:
        if is_structure_outdated(engine):
            logging.critical("ABORTING INIT - Database structure is outdated")
            exit(1)
    logging.info("Database initialized successfully")
    return engine


def create_database_structure(engine: Engine) -> None:
    logging.info("Creating database structure")
    create_all_tables(engine)
    create_version_ref(engine)
    logging.info("Created database structure successfully")


def get_db_engine(url: str) -> Engine:
    logging.info("Initializing database engine")
    if not database_exists(url):
        logging.warning(f"Database does not exist: creating")
        create_database(url)

    logging.debug("Creating database engine")
    engine = create_engine(url)
    logging.info("Database engine initialized successfully")
    return engine


def create_version_ref(engine: Engine) -> None:
    logging.debug(f"Creating version reference: version={VERSION})")
    version_entity = VersionEntity(version=VERSION)
    with Session(engine) as session:
        session.add(version_entity)
        session.commit()
    logging.debug("Created version reference")


def is_structure_outdated(engine: Engine) -> bool:
    logging.debug("Checking if db structure is outdated")
    with Session(engine) as session:
        version = session.query(VersionEntity).first()
        if version.version != VERSION:
            logging.warning("Db structure is outdated!")
            return True
    logging.debug("Db structure is not outdated")
    return False
