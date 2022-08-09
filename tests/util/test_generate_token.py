import logging
from uuid import UUID

from domain.config.model.JWTConfig import JWTConfig
from domain.jwt.adapter.jwt.jwt_adapter import JWTAdapter
from domain.jwt.model.JWTSignCmd import JWTSignCmd


def test_generate_token():
    jwt = JWTAdapter(JWTConfig("HS512", 1800, "DOCKERIZEDhuell"))
    user_id = UUID("c87d57f4-6d0c-4fda-b961-ecdd44be2ce8")
    logging.critical(jwt.sign(JWTSignCmd(user_id)))
