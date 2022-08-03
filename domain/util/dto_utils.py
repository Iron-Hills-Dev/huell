def to_string(_obj: any, _sensitive_fields: list = []) -> str:
    """
    Changes any object to string
    :param _obj: object to change
    :param _sensitive_fields: object's fields that shouldn't be in string
    :return: Ready to print string
    """
    _dict = _obj.__dict__.copy()
    for _field in _sensitive_fields:
        _dict.pop(_field)
    return f"{type(_obj).__name__}{_dict}"


