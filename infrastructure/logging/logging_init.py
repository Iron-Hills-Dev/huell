import logging

from flask import Config

_logging_level_env_ = "HUELL_LOGLEVEL"


def logging_init(_config: Config):
    _loglevel = get_loglevel(_config[_logging_level_env_])
    ch = logging.StreamHandler()
    ch.setLevel(_loglevel)
    ch.setFormatter(CustomFormatter())
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.setLevel(_loglevel)
    logger.addHandler(ch)
    logging.info("Logging activated")


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


def get_loglevel(_loglevel: str):
    match _loglevel:
        case "DEBUG":
            return logging.DEBUG
        case "INFO":
            return logging.INFO
        case "WARN":
            return logging.WARN
        case "ERROR":
            return logging.ERROR
        case "CRITICAL":
            return logging.CRITICAL
        case _:
            logging.critical("ABORTING INIT - unknown HUELL_LOGLEVEL environment variable")
            exit(1)
