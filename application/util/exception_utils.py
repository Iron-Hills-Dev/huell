import logging


def handle_exception(exc) -> tuple:
    logging.debug(f"Handling exception: {exc.code}")
    return {"code": exc.code, "desc": exc.desc}, exc.html_code
