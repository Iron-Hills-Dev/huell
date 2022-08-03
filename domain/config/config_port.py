from abc import ABC, abstractmethod

from domain.config.model.JWTConfig import JWTConfig
from domain.config.model.UserConfig import UserConfig


class ConfigPort(ABC):
    @abstractmethod
    def read_user_config(self) -> UserConfig:
        """
        Converts user config data to UserConfig class
        """
        pass

    @abstractmethod
    def read_jwt_config(self) -> JWTConfig:
        """
        Converts jwt config data to JWTConfig class
        """
        pass
