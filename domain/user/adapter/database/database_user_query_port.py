import logging
from uuid import UUID

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.user.adapter.database.utils.user_utils import entity_to_user
from domain.user.model.User import User
from domain.user.user_query_port import UserQueryPort
from infrastructure.postgres.model.user_entity import UserEntity


class DatabaseUserQueryAdapter(UserQueryPort):
    def __init__(self, _engine_: Engine):
        self._engine_ = _engine_

    def find_user_by_id(self, _id: UUID) -> User:
        logging.debug(f"Searching for user {_id}")
        with Session(self._engine_) as session:
            logging.debug("Database transaction started: searching for user")
            _user_entity = session.query(UserEntity).filter(UserEntity.id == _id).first()
            _user = entity_to_user(_user_entity)
        logging.debug("User found successfully")
        return _user

    def find_user_by_username(self, _username: str) -> User:
        logging.debug(f"Searching for user {_username}")
        with Session(self._engine_) as session:
            logging.debug("Database transaction started: searching for user")
            _user_entity = session.query(UserEntity).filter(UserEntity.username == _username).first()
            _user = entity_to_user(_user_entity)
        logging.debug("User found successfully")
        return _user
