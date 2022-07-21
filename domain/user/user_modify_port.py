from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.User import User
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd


class UserModifyPort(ABC):
    @abstractmethod
    def create_user(self, _cmd: UserCreateCmd) -> UUID:
        pass

    @abstractmethod
    def delete_user(self, _cmd: UserDeleteCmd) -> None:
        pass

    @abstractmethod
    def change_password(self, _cmd: ChangePasswordCmd) -> None:
        pass

    @abstractmethod
    def check_user(self, _user: User, _password: str) -> None:
        pass
