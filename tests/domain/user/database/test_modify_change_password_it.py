from uuid import UUID

import pytest
from argon2 import PasswordHasher

from domain.user.adapter.database.database_user_modify_adapter import DatabaseUserModifyAdapter
from domain.user.adapter.database.database_user_query_adapter import DatabaseUserQueryAdapter
from domain.user.exceptions import AuthError, UserNotFound, PasswordSyntaxError
from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.UserCreateCmd import UserCreateCmd
from tests.decors import using_database


@using_database
def test_change_password_should_change(db_engine):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, query)
    ph = PasswordHasher()

    _cmd = UserCreateCmd("GALJO", "qwertyuiop")
    _id = modify.create_user(_cmd)

    # given
    _cmd = ChangePasswordCmd(_id, "qwertyuiop", "asdfghjkl")

    # when
    modify.change_password(_cmd)

    # then
    _user = query.find_user_by_id(_id)
    assert ph.verify(_user.password, "asdfghjkl")


@using_database
def test_change_password_wrong_old_password(db_engine):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, query)

    _cmd = UserCreateCmd("GALJO", "qwertyuiop")
    _id = modify.create_user(_cmd)

    # given
    _cmd = ChangePasswordCmd(_id, "hihihaha!", "asdfghjkl")

    # when & then
    with pytest.raises(AuthError):
        modify.change_password(_cmd) \
 \
        @using_database


def test_change_password_fake_user(db_engine):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, query)

    # given
    _cmd = ChangePasswordCmd(UUID("0c5390a9-e069-4a15-8186-d41d7be31be4"), "qwertyuiop", "asdfghjkl")

    # when & then
    with pytest.raises(UserNotFound):
        modify.change_password(_cmd)


@using_database
def test_change_password_too_short_passwd(db_engine):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, query)

    _cmd = UserCreateCmd("GALJO", "qwertyuiop")
    _id = modify.create_user(_cmd)

    # given
    _cmd = ChangePasswordCmd(_id, "qwertyuiop", "qwerty")

    # when & then
    with pytest.raises(PasswordSyntaxError):
        modify.change_password(_cmd)


@using_database
def test_change_password_too_long_passwd(db_engine):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, query)

    _cmd = UserCreateCmd("GALJO", "qwertyuiop")
    _id = modify.create_user(_cmd)

    # given
    _cmd = ChangePasswordCmd(_id, "qwertyuiop", "qwertyuiopqwertyuiopqwerty")

    # when & then
    with pytest.raises(PasswordSyntaxError):
        modify.change_password(_cmd)
