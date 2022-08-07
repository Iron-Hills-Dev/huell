import logging
from uuid import uuid4, UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.config.model.UserConfig import UserConfig
from domain.user.exceptions import UserNotFound, UserCreateError, UserDeleteError, ChangePasswordError
from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.User import User
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd
from domain.user.user_modify_port import UserModifyPort
from infrastructure.postgres.user.utils.user_check_utils import check_user, check_password
from infrastructure.postgres.user.utils.user_utils import user_to_entity, get_user_entity

ph = PasswordHasher()


class DatabaseUserModifyAdapter(UserModifyPort):
    def __init__(self, engine: Engine, config: UserConfig):
        self.engine = engine
        self.config = config

    def create_user(self, cmd: UserCreateCmd) -> UUID:
        logging.debug(f"Creating user: {cmd}")
        user = User(uuid4(), cmd.username, ph.hash(cmd.password))
        check_user(self.config, self.engine, user, cmd.password)
        user_entity = user_to_entity(user)
        try:
            with Session(self.engine) as session:
                session.add(user_entity)
                session.commit()
        except Exception as _e:
            logging.error(f"Transaction failed during user creation: exception={_e}")
            raise UserCreateError("User cannot be created")
        logging.debug(f"User was created successfully: {user}")
        return user.id

    def delete_user(self, cmd: UserDeleteCmd) -> None:
        logging.debug(f"Deleting user: {cmd}")
        try:
            with Session(self.engine) as session:
                user_entity = get_user_entity(session, cmd.id)
                session.delete(user_entity)
                session.commit()
        except UserNotFound as e:
            raise e
        except Exception as e:
            logging.error(f"Transaction failed during user deletion: exception={e}")
            raise UserDeleteError("User cannot be deleted")
        logging.debug(f"User was deleted successfully")

    def change_password(self, cmd: ChangePasswordCmd) -> None:
        logging.debug(f"Changing password: {cmd}")
        check_password(self.config, cmd.new_password)
        try:
            with Session(self.engine) as session:
                user_entity = get_user_entity(session, cmd.user_id)
                ph.verify(user_entity.password, cmd.old_password)
                user_entity.password = ph.hash(cmd.new_password)
                session.commit()
            logging.debug(f"Password was successfully changed")
        except UserNotFound as e:
            raise e
        except VerifyMismatchError:
            logging.error("Old password is incorrect")
            raise ChangePasswordError("Incorrect password")
        except Exception as e:
            logging.error(f"Transaction failed during password change: exception={e}")
            raise ChangePasswordError("Password cannot be changed")
