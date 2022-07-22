import logging
from functools import wraps
from time import sleep

from infrastructure.postgres.init_db import create_database_structure
from infrastructure.postgres.model.dec_base import drop_all_tables


def using_database(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        logging.debug("Using test database")
        _engine_ = kwargs["db_engine"]
        create_database_structure(_engine_)
        logging.debug("Starting test")
        try:
            f(*args, **kwargs)
        finally:
            logging.debug("Test finished")
            logging.debug("Clearing database")
            drop_all_tables(_engine_)
            logging.debug("Database cleared")

    return wrapper
