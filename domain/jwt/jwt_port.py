from abc import ABC, abstractmethod

from domain.jwt.model.JWTSignCmd import JWTSignCmd
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd


class JWTPort(ABC):
    @abstractmethod
    def sign(self, _cmd: JWTSignCmd):
        """
        Signs a JWT for user authentication
        :param _cmd: Sign command
        """
        pass

    @abstractmethod
    def decode(self, _cmd: JWTDecodeCmd) -> dict:
        """
        Verifies and decodes given JWT
        :param _cmd: Decode command
        """
        pass
