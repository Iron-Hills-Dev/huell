from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd


class UserModifyPort(ABC):
    @abstractmethod
    def create_user(self, cmd: UserCreateCmd) -> UUID:
        """
        Creates user with data from `cmd` and returns generated user's UUID
        :param cmd: UserCreateCmd class with data to create user
        """
        pass

    @abstractmethod
    def delete_user(self, cmd: UserDeleteCmd) -> None:
        """
        Deletes user indicated in `cmd`
        :param cmd: UserDeleteCmd with data to delete user
        """
        pass

    @abstractmethod
    def change_password(self, cmd: ChangePasswordCmd) -> None:
        """
        Changes password of user indicated in `cmd` to new password in `cmd`
        :param cmd: ChangePasswordCmd with data to change user's password.
        """
        pass
