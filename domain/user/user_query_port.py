from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.model.User import User


class UserQueryPort(ABC):
    @abstractmethod
    def find_user_by_id(self, _id: UUID) -> User:
        pass

    @abstractmethod
    def find_user_by_username(self, _username: str) -> User:
        pass
