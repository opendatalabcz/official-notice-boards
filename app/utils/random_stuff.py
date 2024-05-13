from typing import Any


def return_null_if_empty(text: str | None) -> str | None:
    if not isinstance(text, str) or len(text) == 0:
        return None
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


def split_data_using_transpose(input_data) -> tuple[list[Any], list[Any]]:
    if len(input_data) == 0:
        return [], []
    return tuple(map(list, zip(*input_data)))


def add_count_query_results(results: list[list[tuple[int, str]]]):
    tmp_results = {}
    for input_results in results:
        for count, name in input_results:
            if name not in tmp_results:
                tmp_results[name] = count
            else:
                tmp_results[name] += count
    return sorted([(c, n) for n, c in tmp_results.items()], key=lambda x: x[0], reverse=True)