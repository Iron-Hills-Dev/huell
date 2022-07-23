import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.config.model.UserConfig import UserConfig
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError
from domain.user.model.User import User
from infrastructure.postgres.model.UserEntity import UserEntity


def check_user(_config_: UserConfig, _engine_: Engine, _user: User, _password: str) -> None:
    logging.debug(f"Checking user syntax: {_user}")
    check_username(_config_, _engine_, _user.username)
    check_password(_config_, _password)
    logging.debug("User is correct")


def check_username(_config_: UserConfig, _engine_: Engine, _username: str) -> None:
    logging.debug(f"Checking username: username={_username}")
    if _config_.username_min_len is not None:
        if len(_username) < _config_.username_min_len:
            logging.error(f"Given username is too short ({len(_username)} vs {_config_.username_min_len})")
            raise UsernameSyntaxError(f"Username is too short (min {_config_.username_min_len})")
    if _config_.username_max_len is not None:
        if len(_username) > _config_.username_max_len:
            logging.error(f"Given password is too long ({len(_username)} vs {_config_.username_max_len})")
            raise UsernameSyntaxError(f"Password is too long (max {_config_.username_max_len})")

    if _config_.username_char_wl is not None:
        for _ch in _username:
            if _ch not in _config_.username_char_wl:
                logging.error(f"Given username contains illegal character: {_ch}")
                raise UsernameSyntaxError(f"Username contains illegal character: {_ch}"
                                          f" (character whitelist: '{_config_.username_char_wl}')")
    elif _config_.username_char_bl is not None:
        for _ch in _username:
            if _ch in _config_.username_char_bl:
                logging.error(f"Given username contains illegal character: {_ch}")
                raise UsernameSyntaxError(f"Username contains illegal character: {_ch}"
                                          f" (character blacklist: '{_config_.username_char_bl}')")

    with Session(_engine_) as session:
        _query = session.query(UserEntity).filter(UserEntity.username == _username)
        if len(list(_query)):
            logging.error(f"Chosen username is busy: username={_username}")
            raise UsernameSyntaxError(_desc=f"Username {_username} is busy")
    logging.debug("Username is correct")


def check_password(_config_: UserConfig, _password: str) -> None:
    logging.debug("Checking password")
    if _config_.passwd_min_len is not None:
        if len(_password) < _config_.passwd_min_len:
            logging.error(f"Given password is too short ({len(_password)} vs {_config_.passwd_min_len})")
            raise PasswordSyntaxError(f"Password is too short (min {_config_.passwd_min_len})")
    if _config_.passwd_max_len is not None:
        if len(_password) > _config_.passwd_max_len:
            logging.error(f"Given password is too long ({len(_password)} vs {_config_.passwd_max_len})")
            raise PasswordSyntaxError(f"Password is too long (max {_config_.passwd_max_len})")

    if _config_.passwd_char_wl is not None:
        for _ch in _password:
            if _ch not in _config_.passwd_char_wl:
                logging.error(f"Given password contains illegal character: {_ch}")
                raise PasswordSyntaxError(f"Password contains illegal character: {_ch}"
                                          f" (character whitelist: '{_config_.passwd_char_wl}')")
    elif _config_.passwd_char_bl is not None:
        for _ch in _password:
            if _ch in _config_.passwd_char_bl:
                logging.error(f"Given password contains illegal character: {_ch}")
                raise PasswordSyntaxError(f"Password contains illegal character: {_ch}"
                                          f" (character blacklist: '{_config_.passwd_char_bl}')")
    logging.debug("Password is correct")
