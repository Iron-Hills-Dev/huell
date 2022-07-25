from time import sleep
from uuid import UUID

import pytest

from domain.config.model.JWTConfig import JWTConfig
from domain.jwt.adapter.jwt.jwt_adapter import JWTAdapter
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd
from domain.jwt.model.JWTSignCmd import JWTSignCmd


def test_decode_should_decode():
    # given
    _config = JWTConfig("HS512", 60)
    _port = JWTAdapter(_config, "test")

    _sign_cmd = JWTSignCmd(UUID("bd8b0f75-bdf7-49ec-9de7-abd76e10edf1"))
    _jwt = _port.sign(_sign_cmd)

    _cmd = JWTDecodeCmd(_jwt)

    # when
    _payload = _port.decode(_cmd)

    # then
    assert _payload["user_id"] == str(_sign_cmd.user_id)
    assert type(_payload["birth"]) == float


def test_decode_wrong_secret():
    # given
    _config = JWTConfig("HS512", 60)
    _port = JWTAdapter(_config, "test")

    _sign_cmd = JWTSignCmd(UUID("bd8b0f75-bdf7-49ec-9de7-abd76e10edf1"))
    _jwt = _port.sign(_sign_cmd)

    _cmd = JWTDecodeCmd(_jwt)

    # when & then
    _port = JWTAdapter(_config, "test2")
    with pytest.raises(JWTDecodeError):
        _port.decode(_cmd)


def test_decode_expired_jwt():
    # given
    _config = JWTConfig("HS512", 2)
    _port = JWTAdapter(_config, "test")

    _sign_cmd = JWTSignCmd(UUID("bd8b0f75-bdf7-49ec-9de7-abd76e10edf1"))
    _jwt = _port.sign(_sign_cmd)

    _cmd = JWTDecodeCmd(_jwt)

    # when & then
    with pytest.raises(JWTDecodeError):
        sleep(3)
        _port.decode(_cmd)
