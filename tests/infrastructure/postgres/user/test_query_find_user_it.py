from uuid import UUID

import pytest
from argon2 import PasswordHasher

from infrastructure.postgres.user.database_user_modify_adapter import DatabaseUserModifyAdapter
from infrastructure.postgres.user.database_user_query_adapter import DatabaseUserQueryAdapter
from domain.user.exceptions import UserNotFound
from domain.user.model.UserCreateCmd import UserCreateCmd
from tests.decors import using_database


@using_database
def test_find_user_by_id_should_find(db_engine, user_config):
    # given
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)
    _ph_ = PasswordHasher()
    _cmd = UserCreateCmd("GALJO", "qwerty!")
    _id = modify.create_user(_cmd)

    # when
    _user = query.find_user_by_id(_id)

    # then
    assert _user.id == _id
    assert _user.username == "GALJO"
    assert _ph_.verify(_user.password, "qwerty!")


@using_database
def test_find_user_by_id_fake_user(db_engine):
    # given
    query = DatabaseUserQueryAdapter(db_engine)
    _id = UUID("30278478-1561-424d-8e4d-d0ad72bf867f")

    # when & then
    with pytest.raises(UserNotFound):
        _user = query.find_user_by_id(_id)


@using_database
def test_find_user_by_username_should_find(db_engine, user_config):
    # given
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)
    _ph_ = PasswordHasher()

    _cmd = UserCreateCmd("GALJO", "qwerty!")
    _id = modify.create_user(_cmd)
    _username = "GALJO"

    # when
    _user = query.find_user_by_username(_username)

    # then
    assert _user.id == _id
    assert _user.username == _username
    assert _ph_.verify(_user.password, "qwerty!")


@using_database
def test_find_user_by_username_fake_user(db_engine):
    # given
    query = DatabaseUserQueryAdapter(db_engine)
    _username = "doomsdayIsComing"

    # when & then
    with pytest.raises(UserNotFound):
        query.find_user_by_username(_username)
