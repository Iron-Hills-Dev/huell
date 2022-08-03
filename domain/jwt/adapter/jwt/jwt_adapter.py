import logging
import time

import jwt
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError

from domain.config.model.JWTConfig import JWTConfig
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.jwt_port import JWTPort
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd
from domain.jwt.model.JWTPayload import JWTPayload
from domain.jwt.model.JWTSignCmd import JWTSignCmd


class JWTAdapter(JWTPort):
    def __init__(self, config: JWTConfig):
        self.config = config

    def sign(self, cmd: JWTSignCmd) -> str:
        logging.debug(f"Signing JWT: {cmd}")
        _payload = JWTPayload(
            "HUELL",
            "HUELL",
            int(time.time()) + self.config.exp_time,
            int(time.time()),
            cmd.user_id
        )

        _jwt = jwt.encode(_payload.to_dict(), self.config.secret,
                          algorithm=self.config.algorithm)
        return _jwt

    def decode(self, cmd: JWTDecodeCmd) -> JWTPayload:
        logging.debug(f"Decoding JWT: {cmd}")
        try:
            _payload = jwt.decode(cmd.jwt, self.config.secret, algorithms=self.config.algorithm)
            _payload = JWTPayload(
                _payload["iss"],
                _payload["sub"],
                _payload["exp"],
                _payload["iat"],
                _payload["user_id"]
            )
            return _payload
        except InvalidSignatureError:
            logging.error(f"Invalid JWT signature: {cmd}")
            raise JWTDecodeError("Invalid JWT signature")
        except ExpiredSignatureError:
            logging.error(f"JWT signature has expired: {cmd}")
            raise JWTDecodeError(f"JWT has expired")
        except DecodeError:
            logging.error(f"Invalid JWT syntax: {cmd}")
            raise JWTDecodeError("Invalid JWT syntax")