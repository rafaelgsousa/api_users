def get_value_for_key(dict_select, key_select):
    if isinstance(dict_select, dict):
        if key_select in dict_select:
            return dict_select[key_select]
        else:
            for value in dict_select.values():
                result = get_value_for_key(value, key_select)
                if result is not None:
                    return result
    return None