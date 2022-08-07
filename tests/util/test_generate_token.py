import logging
from uuid import UUID

from domain.config.model.JWTConfig import JWTConfig
from domain.jwt.adapter.jwt.jwt_adapter import JWTAdapter
from domain.jwt.model.JWTSignCmd import JWTSignCmd


def test_generate_token():
    jwt = JWTAdapter(JWTConfig("HS512", 1800, "DOCKERIZEDhuell"))
    user_id = UUID("1b042c8f-a3a1-4e1f-a8a2-a8e5ebf276e9")
    logging.critical(jwt.sign(JWTSignCmd(user_id)))
