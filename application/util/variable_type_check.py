import logging

from application.exceptions import InvalidVariableType


def is_instance(obj: object, _type: type, name: str) -> None:
    """
    If `obj` has other type than `type` raises `InvalidVariableType` exception
    :param obj: Object to check
    :param _type: Excepted type of `obj`
    :param name: Name of _obj in logs and exceptions
    """
    if not isinstance(obj, _type):
        logging.error(f"Invalid type: object={name} type={type(obj)} valid_type={_type}")
        raise InvalidVariableType(f"'{name}' type is invalid ({type(obj)} vs {_type})")
