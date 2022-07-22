import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.config.model.UserConfig import UserConfig
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError
from infrastructure.postgres.model.user_entity import UserEntity


def check_username(_username: str, _config_: UserConfig, _engine_: Engine) -> None:
    logging.debug(f"Checking username {_username}")
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
            if _ch in _config_.username_char_wl:
                logging.error(f"Given username contains illegal character {_ch}")
                raise UsernameSyntaxError(f"Username contains illegal character {_ch}"
                                          f" (character blacklist: '{_config_.username_char_bl}')")

    with Session(_engine_) as session:
        _query = session.query(UserEntity).filter(UserEntity.username == _username)
        if len(list(_query)):
            logging.error("Chosen username is busy")
            raise UsernameSyntaxError(_desc=f"Username {_username} is busy")
    logging.debug("Username is correct")


def check_password(_password: str, _config_: UserConfig) -> None:
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
            if _ch in _config_.passwd_char_wl:
                logging.error(f"Given password contains illegal character: {_ch}")
                raise PasswordSyntaxError(f"Password contains illegal character: {_ch}"
                                          f" (character blacklist: '{_config_.passwd_char_bl}')")
    logging.debug("Password is correct")
