import time
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
    _config = JWTConfig("HS512", 60, "test")
    _port = JWTAdapter(_config)

    _sign_cmd = JWTSignCmd(UUID("bd8b0f75-bdf7-49ec-9de7-abd76e10edf1"))
    _jwt = _port.sign(_sign_cmd)

    _cmd = JWTDecodeCmd(_jwt)

    # when
    _payload = _port.decode(_cmd)

    # then
    assert _payload.user_id == str(_sign_cmd.user_id)
    assert _payload.exp - time.time() > 0
    assert _payload.iss == "HUELL"
    assert _payload.sub == "HUELL"
    assert time.time() - _payload.iat < 60


def test_decode_wrong_secret():
    # given
    _config = JWTConfig("HS512", 60, "test")
    _port = JWTAdapter(_config)

    _sign_cmd = JWTSignCmd(UUID("bd8b0f75-bdf7-49ec-9de7-abd76e10edf1"))
    _jwt = _port.sign(_sign_cmd)

    _cmd = JWTDecodeCmd(_jwt)

    # when & then
    _config = JWTConfig("HS512", 60, "test2")
    _port = JWTAdapter(_config)
    with pytest.raises(JWTDecodeError):
        _port.decode(_cmd)


def test_decode_expired_jwt():
    # given
    _config = JWTConfig("HS512", 2, "test")
    _port = JWTAdapter(_config)

    _sign_cmd = JWTSignCmd(UUID("bd8b0f75-bdf7-49ec-9de7-abd76e10edf1"))
    _jwt = _port.sign(_sign_cmd)

    _cmd = JWTDecodeCmd(_jwt)

    # when & then
    with pytest.raises(JWTDecodeError):
        sleep(3)
        _port.decode(_cmd)


def test_invalid_jwt():
    # given
    config = JWTConfig("HS512", 10, "test")
    port = JWTAdapter(config)
    cmd = JWTDecodeCmd("hello")

    # when & then
    with pytest.raises(JWTDecodeError):
        port.decode(cmd)
