from unittest import mock
from uuid import UUID

from argon2 import PasswordHasher

from application.exceptions import WrongHeaderError
from application.user.exceptions import NoAuthorizationError
from domain.jwt.exceptions import JWTDecodeError
from domain.jwt.model.JWTPayload import JWTPayload
from domain.user.exceptions import UserNotFound
from domain.user.model.User import User


@mock.patch("application.user.user_rest_adapter.query.find_user_by_id")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_create_user_should_create(decode_mock, find_user_mock, client):
    # given
    ph = PasswordHasher()
    find_user_mock.return_value = User(UUID("a9fbc059-19d8-493e-aeeb-4debeed6326d"), "GALJO", ph.hash("qwerty123"))
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, find_user_mock.return_value.id)

    # when
    response = client.get("/user", headers={"Accept": "application/json", "Authorization": "test"})

    # then
    args = find_user_mock.call_args.args
    assert args[0] == find_user_mock.return_value.id
    assert UUID(response.json["id"]) == find_user_mock.return_value.id
    assert response.json["username"] == find_user_mock.return_value.username
    assert len(response.json) == 2


@mock.patch("application.user.user_rest_adapter.query.find_user_by_id")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_create_user_wrong_header(decode_mock, find_user_mock, client):
    # given
    ph = PasswordHasher()
    find_user_mock.return_value = User(UUID("a9fbc059-19d8-493e-aeeb-4debeed6326d"), "GALJO", ph.hash("qwerty123"))
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, find_user_mock.return_value.id)
    error = WrongHeaderError("test")

    # when
    response = client.get("/user", headers={"Accept": "plain/text", "Authorization": "test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_create_user_wrong_authorization(decode_mock, client):
    # given
    error = JWTDecodeError("test")
    decode_mock.side_effect = error

    # when
    response = client.get("/user", headers={"Accept": "application/json", "Authorization": "test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["desc"] == error.desc
    assert response.json["code"] == error.code


def test_create_user_no_authorization(client):
    # given
    error = NoAuthorizationError("test")

    # when
    response = client.get("/user", headers={"Accept": "application/json"})

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.user.user_rest_adapter.query.find_user_by_id")
@mock.patch("application.user.user_rest_adapter.jwt.decode")
def test_create_user_error_handling(decode_mock, find_user_mock, client):
    # given
    error = UserNotFound("test")
    ph = PasswordHasher()
    find_user_mock.return_value = User(UUID("a9fbc059-19d8-493e-aeeb-4debeed6326d"), "GALJO", ph.hash("qwerty123"))
    find_user_mock.side_effect = error
    decode_mock.return_value = JWTPayload("test", "test", 0, 0, find_user_mock.return_value.id)

    # when
    response = client.get("/user", headers={"Accept": "application/json", "Authorization": "test"})

    # then
    assert response.status_code == error.html_code
    assert response.json["desc"] == error.desc
    assert response.json["code"] == error.code
