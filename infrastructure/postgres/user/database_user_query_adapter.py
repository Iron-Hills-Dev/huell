import logging
from uuid import UUID

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.user.exceptions import UserNotFound, UserFindError
from domain.user.model.User import User
from domain.user.user_query_port import UserQueryPort
from infrastructure.postgres.model.UserEntity import UserEntity
from infrastructure.postgres.user.utils.user_utils import entity_to_user, get_user_entity


class DatabaseUserQueryAdapter(UserQueryPort):
    def __init__(self, _engine_: Engine):
        self._engine_ = _engine_

    def find_user_by_id(self, _id: UUID) -> User:
        logging.debug(f"Searching user: id={_id}")
        try:
            with Session(self._engine_) as session:
                user_entity = get_user_entity(session, _id)
                user = entity_to_user(user_entity)
        except UserNotFound as e:
            raise e
        except Exception as e:
            logging.error(f"Transaction failed during password change: exception={e}")
            raise UserFindError("User could not be found: no further information")
        logging.debug(f"User was found successfully: {user}")
        return user

    def find_user_by_username(self, username: str) -> User:
        logging.debug(f"Searching user: username={username}")
        try:
            with Session(self._engine_) as session:
                user_entity = session \
                    .query(UserEntity) \
                    .filter_by(username=username) \
                    .first()
                if user_entity is None:
                    logging.error(f"Given username does not match any user in database: username={username}")
                    raise UserNotFound(f"User {username} does not exist")
                user = entity_to_user(user_entity)
        except UserNotFound as e:
            raise e
        except Exception as e:
            logging.error(f"Transaction failed during password change: exception={e}")
            raise UserFindError("User could not be found: no further information")

        logging.debug(f"User was found successfully: {user}")
        return user
