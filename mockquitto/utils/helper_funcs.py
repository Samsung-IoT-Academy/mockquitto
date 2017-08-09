def merge_dicts(dict1: dict, dict2: dict) -> dict:
    def _generator_dict(dict1, dict2):
        for key in set(dict1.keys()).union(dict2.keys()):
            if key in dict1 and key in dict2:
                if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                    yield (key, dict(merge_dicts(dict1[key], dict2[key])))
                else:
                    yield (key, [dict1[key], dict2[key]])
            elif key in dict1:
                yield (key, dict1[key])
            elif key in dict2:
                yield (key, dict2[key])

    return dict(_generator_dict(dict1, dict2))


def stringify_dict_open(dict) -> str:
    return str(dict)[:-1] + ","