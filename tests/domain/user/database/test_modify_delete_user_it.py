import pytest

from domain.user.adapter.database.database_user_modify_adapter import DatabaseUserModifyAdapter
from domain.user.adapter.database.database_user_query_adapter import DatabaseUserQueryAdapter
from domain.user.exceptions import UserNotFound
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd
from tests.decors import using_database


@using_database
def test_delete_user_should_delete(db_engine):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, query)

    _cmd = UserCreateCmd("GALJO", "qwertyuiop")
    _id = modify.create_user(_cmd)

    # given
    _cmd = UserDeleteCmd(_id)

    # when
    modify.delete_user(_cmd)

    # then
    with pytest.raises(UserNotFound) as _exc:
        query.find_user_by_id(_id)


@using_database
def test_delete_user_fake_user(db_engine):
    query = DatabaseUserQueryAdapter(db_engine)
    modify = DatabaseUserModifyAdapter(db_engine, query)

    # given
    _cmd = UserDeleteCmd("8ba4e672-391b-4e9a-b0a3-c4a4f4b5537e")

    # when & then
    with pytest.raises(UserNotFound):
        modify.delete_user(_cmd)
