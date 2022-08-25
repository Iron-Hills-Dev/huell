from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.model.User import User


class UserQueryPort(ABC):
    @abstractmethod
    def find_user_by_id(self, _id: UUID) -> User:
        """
        Finds user's data using his ID
        :param _id: User's ID
        """
        pass

    @abstractmethod
    def find_user_by_username(self, username: str) -> User:
        """
        Finds user's data using his username
        :param username: User's username
        """
        pass
