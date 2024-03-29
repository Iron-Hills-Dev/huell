import logging
from unittest import mock
from uuid import UUID

import pytest
from argon2 import PasswordHasher

from application.exceptions import WrongHeaderError
from application.user.exceptions import AuthorizationHeaderError
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.model.JWTPayload import JWTPayload
from domain.user.exceptions import UserNotFound, UserFindError
from domain.user.model.User import User

AUTHORIZATION_PREFIX = "Bearer "


@mock.patch("application.user.user_rest_adapter.query.find_user_by_id")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_find_user_should_create(decode_mock, find_user_mock, client):
    # given
    ph = PasswordHasher()
    find_user_mock.return_value = User(UUID("a9fbc059-19d8-493e-aeeb-4debeed6326d"), "GALJO", ph.hash("qwerty123"))
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, find_user_mock.return_value.id)

    # when
    response = client.get("/user",
                          headers={"Accept": "application/json", "Authorization": f"{AUTHORIZATION_PREFIX}test"})

    # then
    args = find_user_mock.call_args.args
    assert args[0] == find_user_mock.return_value.id
    assert UUID(response.json["id"]) == find_user_mock.return_value.id
    assert response.json["username"] == find_user_mock.return_value.username
    assert len(response.json) == 2


@mock.patch("application.user.user_rest_adapter.query.find_user_by_id")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_find_user_wrong_header(decode_mock, find_user_mock, client):
    # given
    ph = PasswordHasher()
    find_user_mock.return_value = User(UUID("a9fbc059-19d8-493e-aeeb-4debeed6326d"), "GALJO", ph.hash("qwerty123"))
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, find_user_mock.return_value.id)
    error = WrongHeaderError("test")

    # when
    response = client.get("/user", headers={"Accept": "plain/text", "Authorization": f"{AUTHORIZATION_PREFIX}test"})

    # then
    logging.critical(response.json)
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_find_user_wrong_token(decode_mock, client):
    # given
    error = JWTDecodeError("test")
    decode_mock.side_effect = error

    # when
    response = client.get("/user",
                          headers={"Accept": "application/json", "Authorization": f"{AUTHORIZATION_PREFIX}test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["desc"] == error.desc
    assert response.json["code"] == error.code


def test_find_user_wrong_authorization(client):
    # given
    error = AuthorizationHeaderError("test")

    # when
    response = client.get("/user",
                          headers={"Accept": "application/json", "Authorization": f"test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


def test_find_user_no_authorization(client):
    # given
    error = AuthorizationHeaderError("test")

    # when
    response = client.get("/user", headers={"Accept": "application/json"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.query.find_user_by_id")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
@pytest.mark.parametrize(
    "error",
    [
        UserNotFound("test"),
        UserFindError("test")
    ]
)
def test_find_user_error_handling(decode_mock, find_user_mock, client, error):
    # given
    ph = PasswordHasher()
    find_user_mock.return_value = User(UUID("a9fbc059-19d8-493e-aeeb-4debeed6326d"), "GALJO", ph.hash("qwerty123"))
    find_user_mock.side_effect = error
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, find_user_mock.return_value.id)

    # when
    response = client.get("/user",
                          headers={"Accept": "application/json", "Authorization": f"{AUTHORIZATION_PREFIX}test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["desc"] == error.desc
    assert response.json["code"] == error.code
