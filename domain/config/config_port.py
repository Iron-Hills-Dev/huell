from abc import ABC, abstractmethod

from domain.config.model.JWTConfig import JWTConfig
from domain.config.model.UserConfig import UserConfig


class ConfigPort(ABC):
    @abstractmethod
    def read_user_config(self, _path: str) -> UserConfig:
        pass

    def read_jwt_config(self, _path: str) -> JWTConfig:
        pass
