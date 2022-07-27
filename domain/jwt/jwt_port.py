from abc import ABC, abstractmethod

from domain.jwt.model.JWTPayload import JWTPayload
from domain.jwt.model.JWTSignCmd import JWTSignCmd
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd


class JWTPort(ABC):
    @abstractmethod
    def sign(self, cmd: JWTSignCmd) -> str:
        """
        Signs a JWT for user authentication
        :param cmd: Sign command
        """
        pass

    @abstractmethod
    def decode(self, cmd: JWTDecodeCmd) -> JWTPayload:
        """
        Verifies and decodes given JWT
        :param cmd: Decode command
        """
        pass
