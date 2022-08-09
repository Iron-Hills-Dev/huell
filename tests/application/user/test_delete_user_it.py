from unittest import mock
from uuid import UUID

import pytest

from application.exceptions import WrongHeaderError
from application.user.exceptions import AuthorizationHeaderError
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.model.JWTPayload import JWTPayload
from domain.user.exceptions import UserNotFound, UserDeleteError

AUTHORIZATION_PREFIX = "Bearer "


@mock.patch("application.user.user_rest_adapter.modify.delete_user")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_delete_user_should_create(decode_mock, delete_user_mock, client):
    # given
    delete_user_mock.return_value = None
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))

    # when
    response = client.delete("/user", headers={"Accept": "text/plain", "Authorization": f"{AUTHORIZATION_PREFIX}test"})

    # then
    args = delete_user_mock.call_args.args
    assert args[0].id == decode_mock.return_value.user_id
    assert response.status_code == 204


@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_delete_user_wrong_header(decode_mock, client):
    # given
    error = WrongHeaderError("test")
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))

    # when
    response = client.delete("/user",
                             headers={"Accept": "application/ogg", "Authorization": f"{AUTHORIZATION_PREFIX}test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.modify.delete_user")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_delete_user_wrong_token(decode_mock, delete_user_mock, client):
    # given
    error = JWTDecodeError("test")
    delete_user_mock.return_value = None
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))
    decode_mock.side_effect = error

    # when
    response = client.delete("/user",
                             headers={"Accept": "application/ogg", "Authorization": f"{AUTHORIZATION_PREFIX}test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


def test_delete_user_wrong_authorization(client):
    # given
    error = AuthorizationHeaderError("test")

    # when
    response = client.delete("/user",
                             headers={"Accept": "application/ogg", "Authorization": f"test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.modify.delete_user")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_delete_user_no_authorization(decode_mock, delete_user_mock, client):
    # given
    error = AuthorizationHeaderError("test")
    delete_user_mock.return_value = None
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))
    # when
    response = client.delete("/user", headers={"Accept": "text/plain"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.modify.delete_user")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
@pytest.mark.parametrize(
    "error",
    [
        UserNotFound("test"),
        UserDeleteError("test")
    ]
)
def test_delete_user_error_handling(decode_mock, delete_user_mock, client, error):
    # given
    delete_user_mock.return_value = None
    delete_user_mock.side_effect = error
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))

    # when
    response = client.delete("/user", headers={"Accept": "text/plain", "Authorization": f"{AUTHORIZATION_PREFIX}test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code
