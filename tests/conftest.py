import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from testcontainers.postgres import PostgresContainer

from app import _app_
from domain.config.model.UserConfig import UserConfig


@pytest.fixture
def client():
    _app_.config.update({"TESTING": True})
    _client = _app_.test_client()
    return _client


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    postgres = PostgresContainer("postgres:14.4")
    postgres.start()
    url = postgres.get_connection_url()
    db_engine = create_engine(url)
    yield db_engine
    postgres.stop()


@pytest.fixture(scope="session")
def user_config() -> UserConfig:
    return UserConfig(username_char_wl="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890.:_-+=",
                        username_min_len=7, username_max_len=16, passwd_min_len=7, passwd_max_len=25)