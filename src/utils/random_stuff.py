from typing import Any


def return_null_if_empty(text: str | None) -> str | None:
    if text == '':
        text = None
    return text


def nested_get(dictionary: dict, keys: list) -> Any | None:
    """servers as nested calls to get() on a dictionary"""
    for key in keys:
        if not isinstance(dictionary, dict):
            return None
        dictionary = dictionary.get(key)
        if dictionary is None:
            return None
    return dictionary
