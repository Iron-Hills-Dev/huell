import logging
from unittest import mock
from uuid import UUID

import pytest

from application.exceptions import WrongHeaderError
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError, UserCreateError


@mock.patch("application.user.user_rest_adapter.modify.create_user")
def test_create_user_should_create(create_user_mock, client):
    # given
    _id = UUID("a20d7a48-7235-489b-8552-5a081d069078")
    create_user_mock.return_value = _id

    # when
    response = client.post("/user", headers={"Accept": "application/json", "Content-Type": "application/json"},
                           json={"username": "GALJO", "password": "qwerty123"})

    # then
    args = create_user_mock.call_args.args
    assert args[0].username == "GALJO"
    assert args[0].password == "qwerty123"
    assert UUID(response.json["userID"]) == _id
    assert len(response.json) == 1


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
    assert response.status_code == 400


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
    assert response.status_code == 400


@mock.patch("application.user.user_rest_adapter.modify.create_user")
@pytest.mark.parametrize(
    "error",
    [
        UsernameSyntaxError("test"),
        PasswordSyntaxError("test"),
        UserCreateError("test"),
    ]
)
def test_create_user_username_error_handling(create_user_mock, error, client):
    logging.info(f"Test is parametrised: error={error}")
    # given
    create_user_mock.return_value = "a20d7a48-7235-489b-8552-5a081d069078"
    create_user_mock.side_effect = error

    # when
    response = client.post("/user", headers={"Accept": "application/json", "Content-Type": "application/json"},
                           json={"username": "GALJO", "password": "qwerty123"})

    # then
    assert response.json["desc"] == error.desc
    assert response.json["code"] == error.code
    assert response.status_code == error.html_code
