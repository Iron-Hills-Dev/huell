import logging

import yaml
from yaml import SafeLoader

from domain.config.config_port import ConfigPort
from domain.config.model.JWTConfig import JWTConfig
from domain.config.model.UserConfig import UserConfig


class YAMLConfigAdapter(ConfigPort):
    def read_user_config(self, _path: str) -> UserConfig:
        logging.debug(f"Reading user config: path={_path}")
        with open(_path) as f:
            _config = yaml.load(f, Loader=SafeLoader)
        _config = UserConfig(_config["user_config"]["username_char_wl"], _config["user_config"]["passwd_char_wl"],
                             _config["user_config"]["username_char_bl"], _config["user_config"]["passwd_char_bl"],
                             _config["user_config"]["passwd_max_len"], _config["user_config"]["passwd_min_len"],
                             _config["user_config"]["username_min_len"], _config["user_config"]["username_max_len"])
        return _config

    def read_jwt_config(self, _path: str) -> JWTConfig:
        logging.debug(f"Reading JWT config: path={_path}")
        with open(_path) as f:
            _config = yaml.load(f, Loader=SafeLoader)
        _config = JWTConfig(_config["jwt_config"]["algorithm"], _config["jwt_config"]["exp_time"])
        return _config
