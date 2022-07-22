import logging
from functools import wraps

from sqlalchemy.orm import Session

from infrastructure.postgres.init_db import create_database_structure
from infrastructure.postgres.model.user_entity import UserEntity
from infrastructure.postgres.model.version_entity import VersionEntity


def using_database(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        logging.debug("Using test database")
        _engine_ = kwargs["db_engine"]
        create_database_structure(_engine_)
        logging.debug("Starting test")

        f(*args, **kwargs)

        logging.debug("Test finished")
        with Session(_engine_) as session:
            logging.debug("Database transaction started: clearing database")
            session.query(UserEntity).delete()
            session.query(VersionEntity).delete()
            session.commit()
        logging.debug("Database cleared")

    return wrapper
