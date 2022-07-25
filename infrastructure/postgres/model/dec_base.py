import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

_base_ = declarative_base()


def create_all_tables(_engine_: Engine) -> None:
    """
    Creates all tables in this declarative base
    :param _engine_: DB engine
    """
    logging.debug("Creating tables")
    _base_.metadata.create_all(_engine_)
    logging.debug("Created tables")


def drop_all_tables(_engine_: Engine) -> None:
    """
    Drops all tables and their contents from this declarative base
    :param _engine_: DB engine
    """
    logging.debug("Dropping tables")
    _base_.metadata.drop_all(_engine_)
    logging.debug("Dropped tables")
