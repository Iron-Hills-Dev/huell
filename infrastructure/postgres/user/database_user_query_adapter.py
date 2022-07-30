import logging
from uuid import UUID

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from infrastructure.postgres.user.utils.user_utils import entity_to_user, get_user_entity
from domain.user.exceptions import UserNotFound
from domain.user.model.User import User
from domain.user.user_query_port import UserQueryPort
from infrastructure.postgres.model.UserEntity import UserEntity


class DatabaseUserQueryAdapter(UserQueryPort):
    def __init__(self, _engine_: Engine):
        self._engine_ = _engine_

    def find_user_by_id(self, _id: UUID) -> User:
        logging.debug(f"Searching user: id={_id}")
        with Session(self._engine_) as session:
            user_entity = get_user_entity(session, _id)
            user = entity_to_user(user_entity)
        logging.debug(f"User was found successfully: {user}")
        return user

    def find_user_by_username(self, username: str) -> User:
        logging.debug(f"Searching user: username={username}")
        with Session(self._engine_) as session:
            user_entity = session \
                .query(UserEntity) \
                .filter_by(username=username) \
                .first()
            if user_entity is None:
                logging.error(f"Given username does not match any user in database: username={username}")
                raise UserNotFound(f"User {username} does not exist")
            user = entity_to_user(user_entity)
        logging.debug(f"User was found successfully: {user}")
        return user
