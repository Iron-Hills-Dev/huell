from unittest import mock
from uuid import UUID

import pytest

from application.exceptions import WrongHeaderError, InvalidVariableType
from application.user.exceptions import AuthorizationHeaderError
from application.user.model.UserChangePasswordRequest import UserChangePasswordRequest
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.model.JWTPayload import JWTPayload
from domain.user.exceptions import UserNotFound, IncorrectPassword, ChangePasswordError

AUTHORIZATION_PREFIX = "Bearer "


@mock.patch("application.user.user_rest_adapter.modify.change_password")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_change_password_should_change(decode_mock, change_password_mock, client):
    # given
    change_password_mock.return_value = None
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))
    body = UserChangePasswordRequest("qwerty123", "qwerty456")

    # when
    response = client.put("/user/change-passwd",
                          headers={"Accept": "*/*", "Content-Type": "application/json",
                                   "Authorization": f"{AUTHORIZATION_PREFIX}test"}, json=body.to_json())

    # then
    args = change_password_mock.call_args.args
    assert args[0].user_id == decode_mock.return_value.user_id
    assert args[0].current_password == body.current_password
    assert args[0].new_password == body.new_password
    assert response.status_code == 204


@mock.patch("application.user.user_rest_adapter.jwt.decode")
@pytest.mark.parametrize(
    "headers",
    [
        ["application/ogg", "application/json"],
        ["text/plain", "application/javascript"]
    ]
)
def test_change_password_wrong_headers(decode_mock, client, headers):
    # given
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))
    error = WrongHeaderError("test")
    body = UserChangePasswordRequest("qwerty123", "qwerty456")

    # when
    response = client.put("/user/change-passwd",
                          headers={"Accept": headers[0], "Content-Type": headers[1],
                                   "Authorization": f"{AUTHORIZATION_PREFIX}test"}, json=body.to_json())

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


def test_change_password_wrong_authorization(client):
    # given
    error = AuthorizationHeaderError("test")
    body = UserChangePasswordRequest("qwerty123", "qwerty456")

    # when
    response = client.put("/user/change-passwd",
                          headers={"Accept": "text/plain", "Content-Type": "application/json",
                                   "Authorization": f"test"}, json=body.to_json())

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_change_password_wrong_token(decode_mock, client):
    # given
    error = JWTDecodeError("test")
    body = UserChangePasswordRequest("qwerty123", "qwerty456")
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))

    decode_mock.side_effect = error

    # when
    response = client.put("/user/change-passwd",
                          headers={"Accept": "text/plain", "Content-Type": "application/json",
                                   "Authorization": f"{AUTHORIZATION_PREFIX}test"}, json=body.to_json())

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


def test_change_password_no_authorization(client):
    # given
    error = AuthorizationHeaderError("test")
    body = UserChangePasswordRequest("qwerty123", "qwerty456")

    # when
    response = client.put("/user/change-passwd",
                          headers={"Accept": "text/plain", "Content-Type": "application/json"}, json=body.to_json())

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.modify.change_password")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
@pytest.mark.parametrize(
    "error",
    [
        UserNotFound("test"),
        IncorrectPassword("test"),
        ChangePasswordError("test")
    ]
)
def test_change_password_error_handling(decode_mock, change_password_mock, client, error):
    # given
    change_password_mock.return_value = None
    change_password_mock.side_effect = error
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))
    body = UserChangePasswordRequest("qwerty123", "qwerty456")

    # when
    response = client.put("/user/change-passwd",
                          headers={"Accept": "*/*", "Content-Type": "application/json",
                                   "Authorization": f"{AUTHORIZATION_PREFIX}test"}, json=body.to_json())

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.modify.change_password")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
@pytest.mark.parametrize(
    "body",
    [
        {"currentPassword": 1, "newPassword": "qwerty123"},
        {"currentPassword": "qwerty123", "newPassword": 1}
    ]
)
def test_change_password_invalid_variable(decode_mock, change_password_mock, client, body):
    # given
    error = InvalidVariableType("test")
    change_password_mock.return_value = None
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, UUID("be964b8c-59cf-4549-9f25-eb6bb63824ec"))

    # when
    response = client.put("/user/change-passwd",
                          headers={"Accept": "*/*", "Content-Type": "application/json",
                                   "Authorization": f"{AUTHORIZATION_PREFIX}test"}, json=body)

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code
