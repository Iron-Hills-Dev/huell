from abc import ABC, abstractmethod

from domain.config.model.UserConfig import UserConfig


class ConfigPort(ABC):
    @abstractmethod
    def read_user_config(self, _path: str) -> UserConfig:
        pass
