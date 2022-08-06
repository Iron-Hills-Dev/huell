import logging
from unittest import mock

import pytest
from argon2 import PasswordHasher

from application.exceptions import WrongHeaderError
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError, UserCreateError


@mock.patch("application.user.user_rest_adapter.modify.create_user")
def test_create_user_should_create(create_user_mock, client):
    # given
    user_id = "a20d7a48-7235-489b-8552-5a081d069078"
    ph = PasswordHasher()
    create_user_mock.return_value = user_id

    # when
    response = client.post("/user", headers={"Accept": "application/json", "Content-Type": "application/json"},
                           json={"username": "GALJO", "password": "qwerty123"})

    # then
    args = create_user_mock.call_args.args
    assert args[0].username == "GALJO"
    assert args[0].password == "qwerty123"
    assert response.json["userID"] == user_id


@pytest.mark.parametrize(
    "test_input",
    [([1, "qwerty123"]), (["GALJO", 1])]
)
def test_create_user_invalid_variable_type(test_input, client):
    logging.info(f"Test is parametrised: test_input={test_input}")
    # when
    response = client.post("/user", headers={"Accept": "application/json", "Content-Type": "application/json"},
                           json={"username": test_input[0], "password": test_input[1]})

    # then
    assert response.json["code"] == "APP.IVT"


@pytest.mark.parametrize(
    "test_input",
    [(["plain/text", "application/json"]), (["application/json", "plain/text"])]
)
def test_create_user_invalid_headers(test_input, client):
    logging.info(f"Test is parametrised: test_input={test_input}")
    # when
    response = client.post("/user", headers={"Accept": test_input[0], "Content-Type": test_input[1]},
                           json={"username": "GALJO", "password": "qwerty123"})

    # then
    assert response.json["code"] == WrongHeaderError("").code


@mock.patch("application.user.user_rest_adapter.modify.create_user")
@pytest.mark.parametrize(
    "error,excepted",
    [(UsernameSyntaxError("test"), UsernameSyntaxError("").code),
     (PasswordSyntaxError("test"), PasswordSyntaxError("").code), (UserCreateError("test"), UserCreateError("").code)]
)
def test_create_user_username_error_handling(create_user_mock, error, excepted, client):
    logging.info(f"Test is parametrised: error={error}, excepted={excepted}")
    # given
    user_id = "a20d7a48-7235-489b-8552-5a081d069078"
    ph = PasswordHasher()
    create_user_mock.return_value = user_id
    create_user_mock.side_effect = error

    # when
    response = client.post("/user", headers={"Accept": "application/json", "Content-Type": "application/json"},
                           json={"username": "GALJO", "password": "qwerty123"})

    # then
    assert response.json["desc"] == "test"
    assert response.json["code"] == excepted
