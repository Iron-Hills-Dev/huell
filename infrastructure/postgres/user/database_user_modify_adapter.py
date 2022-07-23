import logging
from uuid import uuid4, UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.config.model.UserConfig import UserConfig
from infrastructure.postgres.user.utils.user_check_utils import check_user, check_password
from infrastructure.postgres.user.utils.user_utils import user_to_entity, get_user_entity
from domain.user.exceptions import UserNotFound, UserCreateError, UserDeleteError, ChangePasswordError
from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.User import User
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd
from domain.user.user_modify_port import UserModifyPort
from domain.user.user_query_port import UserQueryPort

_ph_ = PasswordHasher()


class DatabaseUserModifyAdapter(UserModifyPort):
    def __init__(self, _engine_: Engine, _config_: UserConfig, _user_query_port: UserQueryPort):
        self._engine_ = _engine_
        self._config_ = _config_
        self.query = _user_query_port

    def create_user(self, _cmd: UserCreateCmd) -> UUID:
        logging.debug(f"Creating user: {_cmd}")
        _user = User(uuid4(), _cmd.username, _ph_.hash(_cmd.password))
        check_user(self._config_, self._engine_, _user, _cmd.password)
        _user_entity = user_to_entity(_user)
        try:
            with Session(self._engine_) as session:
                session.add(_user_entity)
                session.commit()
        except Exception as _e:
            logging.error(f"Transaction failed during user creation: exception={_e}")
            raise UserCreateError("User cannot be created")
        logging.debug(f"User was created successfully: {_user}")
        return _user.id

    def delete_user(self, _cmd: UserDeleteCmd) -> None:
        logging.debug(f"Deleting user: {_cmd}")
        try:
            with Session(self._engine_) as session:
                _user_entity = get_user_entity(session, _cmd.id)
                session.delete(_user_entity)
                session.commit()
        except UserNotFound:
            raise UserDeleteError("User cannot be deleted - user does not exist")
        except Exception as _e:
            logging.error(f"Transaction failed during user deletion: exception={_e}")
            raise UserDeleteError("User cannot be deleted")
        logging.debug(f"User was deleted successfully")

    def change_password(self, _cmd: ChangePasswordCmd) -> None:
        logging.debug(f"Changing password: {_cmd}")
        check_password(self._config_, _cmd.new_password)
        try:
            with Session(self._engine_) as session:
                _user_entity = get_user_entity(session, _cmd.user_id)
                _ph_.verify(_user_entity.password, _cmd.old_password)
                _user_entity.password = _ph_.hash(_cmd.new_password)
                session.commit()
            logging.debug(f"Password was successfully changed")
        except UserNotFound:
            raise ChangePasswordError("User cannot be deleted - user does not exist")
        except VerifyMismatchError:
            logging.error("Old password is incorrect")
            raise ChangePasswordError("Incorrect password")
        except Exception as _e:
            logging.error(f"Transaction failed during password change: exception={_e}")
            raise ChangePasswordError("Password cannot be changed")
