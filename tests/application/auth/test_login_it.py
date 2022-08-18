from unittest import mock
from uuid import UUID

import pytest

from application.auth.exceptions import AuthError
from application.auth.model.UserLoginRequest import UserLoginRequest
from application.exceptions import WrongHeaderError
from domain.user.exceptions import UserNotFound
from domain.user.model.User import User


@mock.patch("application.auth.auth_rest_adapter.jwt.sign")
@mock.patch("application.auth.auth_rest_adapter.user_query.find_user_by_username")
def test_login_should_login(find_user_mock, sign_mock, client):
    # given
    user = User(
        UUID("39568624-5fc1-452c-aeaa-80cf798e99c8"),
        "GALJO",
        "$argon2i$v=19$m=16,t=2,p=1$eGR4ZHhkeGR4ZA$QN9XB7ESgoOhzA5Z4oLWvg")
    jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9"
    ".eyJpc3MiOiJIVUVMTCIsInN1YiI6IkhVRUxMIiwiZXhwIjoxNjYwMDUyMzc5LCJpYXQiOjE2NjAwNTA1NzksInVzZXJfaWQiOiIzOTU2ODY"
    "yNC01ZmMxLTQ1MmMtYWVhYS04MGNmNzk4ZTk5YzgifQ"
    ".4E1GXuTIOVYECPG8oj1bhiQ69TC3xaO31Yfer_NI8ljiH9gTt2MzC9rpLfM-trgPVmVDx0scpPYejox3EWopag"

    find_user_mock.return_value = user
    sign_mock.return_value = jwt

    request = UserLoginRequest("GALJO", "qwerty123")

    # when
    response = client.post("/login",
                           headers={"Accept": "application/json", "Content-Type": "application/json"},
                           json=request.to_json())

    # then
    find_user_args = find_user_mock.call_args.args
    sign_args = sign_mock.call_args.args
    response_content = response.get_json()

    assert find_user_args[0] == user.username
    assert sign_args[0].user_id == user.id
    assert response_content["token"] == jwt
    assert response.status_code == 200


@pytest.mark.parametrize(
    "headers",
    [
        {"Accept": "application/json", "Content-Type": "text/plain"},
        {"Accept": "application/ogg", "Content-Type": "application/json"}
    ]
)
def test_login_wrong_headers(client, headers):
    # given
    request = UserLoginRequest("GALJO", "qwerty123")
    error = WrongHeaderError("test")

    # when
    response = client.post("/login",
                           headers=headers,
                           json=request.to_json())

    # then
    assert response.status_code == error.html_code
    assert response.json["code"] == error.code


@mock.patch("application.auth.auth_rest_adapter.jwt.sign")
@mock.patch("application.auth.auth_rest_adapter.user_query.find_user_by_username")
@pytest.mark.parametrize(
    "error,excepted",
    [
        (UserNotFound("test"), AuthError("Incorrect username or password"))
    ]
)
def test_login_error_handling_find_user(find_user_mock, sign_mock, client, error, excepted):
    # given
    user = User(
        UUID("39568624-5fc1-452c-aeaa-80cf798e99c8"),
        "GALJO",
        "$argon2i$v=19$m=16,t=2,p=1$eGR4ZHhkeGR4ZA$QN9XB7ESgoOhzA5Z4oLWvg")
    jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9"
    ".eyJpc3MiOiJIVUVMTCIsInN1YiI6IkhVRUxMIiwiZXhwIjoxNjYwMDUyMzc5LCJpYXQiOjE2NjAwNTA1NzksInVzZXJfaWQiOiIzOTU2ODY"
    "yNC01ZmMxLTQ1MmMtYWVhYS04MGNmNzk4ZTk5YzgifQ"
    ".4E1GXuTIOVYECPG8oj1bhiQ69TC3xaO31Yfer_NI8ljiH9gTt2MzC9rpLfM-trgPVmVDx0scpPYejox3EWopag"

    find_user_mock.return_value = user
    find_user_mock.side_effect = error
    sign_mock.return_value = jwt

    request = UserLoginRequest("GALJO", "qwerty123")

    # when
    response = client.post("/login",
                           headers={"Accept": "application/json", "Content-Type": "application/json"},
                           json=request.to_json())

    # then
    response_content = response.get_json()

    assert response_content["code"] == excepted.code
    assert response_content["desc"] == excepted.desc
    assert response.status_code == excepted.html_code


@mock.patch("application.auth.auth_rest_adapter.jwt.sign")
@mock.patch("application.auth.auth_rest_adapter.user_query.find_user_by_username")
def test_login_wrong_password(find_user_mock, sign_mock, client):
    # given
    user = User(
        UUID("39568624-5fc1-452c-aeaa-80cf798e99c8"),
        "GALJO",
        "$argon2i$v=19$m=16,t=2,p=1$eGR4ZHhkeGR4ZA$QN9XB7ESgoOhzA5Z4oLWvg")
    jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9"
    ".eyJpc3MiOiJIVUVMTCIsInN1YiI6IkhVRUxMIiwiZXhwIjoxNjYwMDUyMzc5LCJpYXQiOjE2NjAwNTA1NzksInVzZXJfaWQiOiIzOTU2ODY"
    "yNC01ZmMxLTQ1MmMtYWVhYS04MGNmNzk4ZTk5YzgifQ"
    ".4E1GXuTIOVYECPG8oj1bhiQ69TC3xaO31Yfer_NI8ljiH9gTt2MzC9rpLfM-trgPVmVDx0scpPYejox3EWopag"

    error = AuthError("Incorrect username or password")

    find_user_mock.return_value = user
    sign_mock.return_value = jwt

    request = UserLoginRequest("GALJO", "qwerty1234")

    # when
    response = client.post("/login",
                           headers={"Accept": "application/json", "Content-Type": "application/json"},
                           json=request.to_json())

    # then
    response_content = response.get_json()

    assert response_content["code"] == error.code
    assert response_content["desc"] == error.desc
    assert response.status_code == error.html_code
