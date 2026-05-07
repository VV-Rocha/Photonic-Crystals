def _object_has_dict_attributes(value):
    if not hasattr(value, "__dict__"):
        return False

    for attr_value in vars(value).values():
        if isinstance(attr_value, dict):
            return True

    return False