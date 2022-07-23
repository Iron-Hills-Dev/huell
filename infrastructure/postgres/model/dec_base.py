import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

_base_ = declarative_base()


def create_all_tables(_engine_: Engine):
    logging.debug("Creating tables")
    _base_.metadata.create_all(_engine_)
    logging.debug("Created tables")


def drop_all_tables(_engine_: Engine):
    logging.debug("Dropping tables")
    _base_.metadata.drop_all(_engine_)
    logging.debug("Dropped tables")
