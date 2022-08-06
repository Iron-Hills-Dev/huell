import logging
from uuid import UUID

from domain.config.model.JWTConfig import JWTConfig
from domain.jwt.adapter.jwt.jwt_adapter import JWTAdapter
from domain.jwt.model.JWTSignCmd import JWTSignCmd


def test_generate_token():
    jwt = JWTAdapter(JWTConfig("HS512", 1800, "DOCKERIZEDhuell"))
    user_id = UUID("a9fbc059-19d8-493e-aeeb-4debeed6326d")
    logging.critical(jwt.sign(JWTSignCmd(user_id)))
