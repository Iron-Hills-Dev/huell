from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd


class UserModifyPort(ABC):
    @abstractmethod
    def create_user(self, cmd: UserCreateCmd) -> UUID:
        pass

    @abstractmethod
    def delete_user(self, cmd: UserDeleteCmd) -> None:
        pass

    @abstractmethod
    def change_password(self, cmd: ChangePasswordCmd) -> None:
        pass
