from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd


class UserModifyPort(ABC):
    @abstractmethod
    def create_user(self, _cmd: UserCreateCmd) -> UUID:
        """
        Creates User object
        :param _cmd: Command with user's data
        """
        pass

    @abstractmethod
    def delete_user(self, _cmd: UserDeleteCmd) -> None:
        """
        Deletes user from existence
        :param _cmd: Delete command with needed data
        """
        pass

    @abstractmethod
    def change_password(self, _cmd: ChangePasswordCmd) -> None:
        """
        Changes user password
        :param _cmd: Command with needed data
        """
        pass
