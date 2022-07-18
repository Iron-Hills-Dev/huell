import logging

from flask import Config

_logging_level_env_ = "HUELL_LOGLEVEL"



def logging_init(_config: Config):
    _handler = get_logging_handler(_config[_logging_level_env_])
    _logger = create_logger(_handler)
    logging.info("Logging activated")
    return _logger


class CustomFormatter(logging.Formatter):
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format = "[%(asctime)s] [%(levelname)s] [%(process)s] || [%(threadName)s] %(filename)s :: %(message)s"

    FORMATS = {
        logging.DEBUG: format + reset,
        logging.INFO: format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logging_handler(_loglevel: str) -> logging.StreamHandler:
    ch = logging.StreamHandler()
    match _loglevel:
        case "DEBUG":
            _loglevel = logging.DEBUG
        case "INFO":
            _loglevel = logging.INFO
        case "WARN":
            _loglevel = logging.WARN
        case "ERROR":
            _loglevel = logging.ERROR
        case "CRITICAL":
            _loglevel = logging.CRITICAL
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    return ch


def create_logger(_handler: logging.StreamHandler) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_handler)
    return logger
