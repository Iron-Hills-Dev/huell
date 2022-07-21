import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError
from infrastructure.postgres.model.user_entity import UserEntity


def check_username(_username: str, _engine_: Engine) -> None:
    logging.debug(f"Checking username {_username}")
    if len(_username) > 16 or len(_username) < 4:
        logging.error(f"Username length is wrong {len(_username)}")
        raise UsernameSyntaxError(_desc="Wrong username length (min 4 max 16)")
    # TODO whitelista znakow kiedys i configurowalny check
    with Session(_engine_) as session:
        _query = session.query(UserEntity).filter(UserEntity.username == _username)
        if len(_query):
            logging.error("Chosen username is busy")
            raise UsernameSyntaxError(_desc=f"Username {_username} is busy")
    logging.debug("Username is correct")


def check_password(_password: str) -> None:
    logging.debug("Checking password")
    if len(_password) < 7 or len(_password) > 25:
        logging.error(f"Password length is wrong {len(_password)}")
        raise PasswordSyntaxError(_desc="Wrong password length (min 7 max 25)")
    # TODO tez whitelista znakow i tez configurowalne to ma byc
    logging.debug("Password is correct")

