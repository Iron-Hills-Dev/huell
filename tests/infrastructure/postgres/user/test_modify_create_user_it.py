import pytest
from argon2 import PasswordHasher

from domain.config.model.UserConfig import UserConfig
from infrastructure.postgres.user.database_user_modify_adapter import DatabaseUserModifyAdapter
from infrastructure.postgres.user.database_user_query_adapter import DatabaseUserQueryAdapter
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError
from domain.user.model.UserCreateCmd import UserCreateCmd
from tests.decors import using_database


@using_database
def test_create_user_should_create(db_engine, user_config):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)
    ph = PasswordHasher()

    # given
    _cmd = UserCreateCmd("GALJO", "qwerty!")

    # when
    _id = modify.create_user(_cmd)

    # then
    _user = query.find_user_by_id(_id)
    assert _user.id == _id
    assert _user.username == "GALJO"
    assert ph.verify(_user.password, "qwerty!")


@using_database
def test_create_user_too_short_username(db_engine, user_config):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GAL", "qwerty!")

    # when & then
    with pytest.raises(UsernameSyntaxError) as _exc:
        modify.create_user(_cmd)


@using_database
def test_create_user_too_long_username(db_engine, user_config):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GALJOGALJOGALJOOO", "qwerty!")

    # when & then
    with pytest.raises(UsernameSyntaxError) as _exc:
        modify.create_user(_cmd)


@using_database
def test_create_user_busy_username(db_engine, user_config):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GALJO", "qwerty!")

    # when & then
    with pytest.raises(UsernameSyntaxError) as _exc:
        modify.create_user(_cmd)
        modify.create_user(_cmd)


@using_database
def test_create_user_too_short_passwd(db_engine, user_config):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GALJO", "qwerty")

    # when & then
    with pytest.raises(PasswordSyntaxError) as _exc:
        modify.create_user(_cmd)


@using_database
def test_create_user_too_long_passwd(db_engine, user_config):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GALJO", "qwertyuiopqwertyuiopqwerty")

    # when & then
    with pytest.raises(PasswordSyntaxError) as _exc:
        modify.create_user(_cmd)


@using_database
def test_create_user_used_illegal_char_in_passwd_wl(db_engine):
    user_config = UserConfig(passwd_char_wl="abc")
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GALJO", "abc!cba")

    # when & then
    with pytest.raises(PasswordSyntaxError) as _exc:
        modify.create_user(_cmd)


@using_database
def test_create_user_used_illegal_char_in_passwd_bl(db_engine):
    user_config = UserConfig(passwd_char_bl="/Jx")
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GALJO", "abcdefghiJkl")

    # when & then
    with pytest.raises(PasswordSyntaxError) as _exc:
        modify.create_user(_cmd)


@using_database
def test_create_user_used_illegal_char_in_username_wl(db_engine):
    user_config = UserConfig(username_char_wl="abc")
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GALJO", "abc_abc")

    # when & then
    with pytest.raises(UsernameSyntaxError) as _exc:
        modify.create_user(_cmd)


@using_database
def test_create_user_used_illegal_char_in_username_bl(db_engine):
    user_config = UserConfig(username_char_bl="y#l")
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, user_config, query)

    # given
    _cmd = UserCreateCmd("GAL#JO", "qwerty!")

    # when & then
    with pytest.raises(UsernameSyntaxError) as _exc:
        modify.create_user(_cmd)
