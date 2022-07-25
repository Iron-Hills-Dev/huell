def to_string(_obj: any, _sensitive_fields: list = []) -> str:
    """
    Function for classes __str__ superfunction
    :param _obj: class object (self)
    :param _sensitive_fields: fields that should be deleted from return
    :return: String, that is ready to go public
    """
    _dict = _obj.__dict__.copy()
    for _field in _sensitive_fields:
        _dict.pop(_field)
    return f"{type(_obj).__name__}{_dict}"


