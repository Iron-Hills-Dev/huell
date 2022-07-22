import logging
from uuid import uuid4, UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.config.model.UserConfig import UserConfig
from domain.user.adapter.database.utils.check_user import check_password, check_user
from domain.user.adapter.database.utils.user_utils import user_to_entity
from domain.user.exceptions import AuthError, UserNotFound
from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.User import User
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd
from domain.user.user_modify_port import UserModifyPort
from domain.user.user_query_port import UserQueryPort
from infrastructure.postgres.model.UserEntity import UserEntity

_ph_ = PasswordHasher()


class DatabaseUserModifyAdapter(UserModifyPort):
    def __init__(self, _engine_: Engine, _config_: UserConfig, _user_query_port: UserQueryPort):
        self._engine_ = _engine_
        self._config_ = _config_
        self.query = _user_query_port

    def create_user(self, _cmd: UserCreateCmd) -> UUID:
        logging.debug(f"Creating user")
        _user = User(uuid4(), _cmd.username, _ph_.hash(_cmd.password))
        check_user(self._config_, self._engine_, _user, _cmd.password)
        _user_entity = user_to_entity(_user)
        with Session(self._engine_) as session:
            session.add(_user_entity)
            session.commit()
        logging.debug(f"User {_user.id} created successfully")
        return _user.id

    def delete_user(self, _cmd: UserDeleteCmd) -> None:
        logging.debug(f"Deleting user: id={_cmd.id}")
        with Session(self._engine_) as session:
            _user_entity = session \
                .query(UserEntity) \
                .get(_cmd.id)
            if _user_entity is None:
                logging.error("Given ID does not match any user in database")
                raise UserNotFound(f"User with ID {_cmd.id} does not exist")
            session.delete(_user_entity)
            session.commit()
        logging.debug(f"User deleted successfully")

    def change_password(self, _cmd: ChangePasswordCmd) -> None:
        try:
            logging.debug(f"Changing password: user_id={_cmd.user_id}")
            _user = self.query.find_user_by_id(_cmd.user_id)
            _ph_.verify(_user.password, _cmd.old_password)
            check_password(self._config_, _cmd.new_password)
            with Session(self._engine_) as session:
                _user_entity = session.query(UserEntity).filter(UserEntity.id == _cmd.user_id).first()
                _user_entity.password = _ph_.hash(_cmd.new_password)
                session.commit()
            logging.debug(f"Password successfully changed")
        except VerifyMismatchError:
            logging.error("Old password is incorrect")
            raise AuthError("Incorrect password")
