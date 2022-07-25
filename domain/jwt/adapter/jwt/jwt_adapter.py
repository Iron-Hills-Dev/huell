import logging
import time

import jwt
from jwt import InvalidSignatureError

from domain.config.model.JWTConfig import JWTConfig
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.jwt_port import JWTPort
from domain.jwt.model.JWTAge import JWTAge
from domain.jwt.model.JWTSignCmd import JWTSignCmd
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd


class JWTAdapter(JWTPort):
    def __init__(self, config: JWTConfig, secret: str):
        self.config = config
        self.secret = secret

    def sign(self, _cmd: JWTSignCmd) -> str:
        logging.debug(f"Signing JWT: {_cmd}")
        _jwt = jwt.encode({"user_id": str(_cmd.user_id), "birth": time.time()}, self.secret,
                          algorithm=self.config.algorithm)
        return _jwt

    def decode(self, _cmd: JWTDecodeCmd) -> dict:
        logging.debug("Decoding JWT")
        try:
            _payload = jwt.decode(_cmd.jwt, self.secret, algorithms=self.config.algorithm)
            if time.time() - _payload["birth"] > self.config.exp_time:
                age = JWTAge(_payload["birth"])
                logging.error("JWT is expired")
                raise JWTDecodeError(f"JWT is expired: {age}")
            return _payload
        except JWTDecodeError as e:
            raise e
        except InvalidSignatureError:
            logging.error("Wrong JWT signature")
            raise JWTDecodeError("Wrong JWT signature")
