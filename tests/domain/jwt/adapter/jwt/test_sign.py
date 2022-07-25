from uuid import UUID

from domain.config.model.JWTConfig import JWTConfig
from domain.jwt.adapter.jwt.jwt_adapter import JWTAdapter
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd
from domain.jwt.model.JWTSignCmd import JWTSignCmd


def test_sign_should_sign():
    # given
    _secret = "test"
    _config = JWTConfig("HS512", 60)
    _port = JWTAdapter(_config, "test")
    _cmd = JWTSignCmd(UUID("bd8b0f75-bdf7-49ec-9de7-abd76e10edf1"))

    # when
    _jwt = _port.sign(_cmd)

    # then
    _payload = _port.decode(JWTDecodeCmd(_jwt))
    assert _payload["user_id"] == str(_cmd.user_id)
    assert type(_payload["birth"]) == float
