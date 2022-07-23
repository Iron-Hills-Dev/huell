def to_string(_obj: any, _sensitive_fields: list = []) -> str:
    _dict = _obj.__dict__.copy()
    for _field in _sensitive_fields:
        _dict.pop(_field)
    return f"{type(_obj).__name__}{_dict}"


