import logging

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from domain.config.model.UserConfig import UserConfig
from domain.user.exceptions import UsernameSyntaxError, PasswordSyntaxError
from domain.user.model.User import User
from infrastructure.postgres.model.UserEntity import UserEntity


def check_user(config: UserConfig, engine: Engine, user: User, password: str) -> None:
    logging.debug(f"Checking user syntax: {user}")
    check_username(config, engine, user.username)
    check_password(config, password)
    logging.debug("User is correct")


def check_username(config: UserConfig, engine: Engine, username: str) -> None:
    logging.debug(f"Checking username: username={username}")
    if config.username_min_len != -1:
        if len(username) < config.username_min_len:
            logging.error(f"Given username is too short ({len(username)} vs {config.username_min_len})")
            raise UsernameSyntaxError(f"Username is too short (min {config.username_min_len})")
    if config.username_max_len != -1:
        if len(username) > config.username_max_len:
            logging.error(f"Given password is too long ({len(username)} vs {config.username_max_len})")
            raise UsernameSyntaxError(f"Password is too long (max {config.username_max_len})")

    if config.username_char_wl != "":
        for _ch in username:
            if _ch not in config.username_char_wl:
                logging.error(f"Given username contains illegal character: {_ch}")
                raise UsernameSyntaxError(f"Username contains illegal character: {_ch}"
                                          f" (character whitelist: '{config.username_char_wl}')")
    elif config.username_char_bl != "":
        for _ch in username:
            if _ch in config.username_char_bl:
                logging.error(f"Given username contains illegal character: {_ch}")
                raise UsernameSyntaxError(f"Username contains illegal character: {_ch}"
                                          f" (character blacklist: '{config.username_char_bl}')")

    with Session(engine) as session:
        _query = session.query(UserEntity).filter_by(username=username)
        if len(list(_query)):
            logging.error(f"Chosen username is busy: username={username}")
            raise UsernameSyntaxError(_desc=f"Username {username} is busy")
    logging.debug("Username is correct")


def check_password(_config_: UserConfig, _password: str) -> None:
    logging.debug("Checking password")
    if _config_.passwd_min_len != -1:
        if len(_password) < _config_.passwd_min_len:
            logging.error(f"Given password is too short ({len(_password)} vs {_config_.passwd_min_len})")
            raise PasswordSyntaxError(f"Password is too short (min {_config_.passwd_min_len})")
    if _config_.passwd_max_len != -1:
        if len(_password) > _config_.passwd_max_len:
            logging.error(f"Given password is too long ({len(_password)} vs {_config_.passwd_max_len})")
            raise PasswordSyntaxError(f"Password is too long (max {_config_.passwd_max_len})")

    if _config_.passwd_char_wl != "":
        for _ch in _password:
            if _ch not in _config_.passwd_char_wl:
                logging.error(f"Given password contains illegal character: {_ch}")
                raise PasswordSyntaxError(f"Password contains illegal character: {_ch}"
                                          f" (character whitelist: '{_config_.passwd_char_wl}')")
    elif _config_.passwd_char_bl != "":
        for _ch in _password:
            if _ch in _config_.passwd_char_bl:
                logging.error(f"Given password contains illegal character: {_ch}")
                raise PasswordSyntaxError(f"Password contains illegal character: {_ch}"
                                          f" (character blacklist: '{_config_.passwd_char_bl}')")
    logging.debug("Password is correct")
