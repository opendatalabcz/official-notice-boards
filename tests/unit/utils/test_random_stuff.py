import pytest

from app.utils.random_stuff import return_null_if_empty, nested_get, split_data_using_transpose


@pytest.mark.parametrize('data', [
    {  # non-empty string
        'input_data': "just some text",
        'expected_data': "just some text"
    },
    {  # None
        'input_data': None,
        'expected_data': None
    },
    {  # Empty String
        'input_data': '',
        'expected_data': None
    },
])
def test_return_null_if_empty(data):
    assert data['expected_data'] == return_null_if_empty(data['input_data'])


@pytest.mark.parametrize('data', [
    {  # 2 keys
        'input_dict': {'a': {'b': 'c'}},
        'key_list': ['a', 'b'],
        'expected_data': 'c'
    },
    {  # 1 key, return str
        'input_dict': {'a': 'b'},
        'key_list': ['a'],
        'expected_data': 'b'
    },
    {  # 1 key, return dict
        'input_dict': {'a': {'b': 'c'}},
        'key_list': ['a'],
        'expected_data': {'b': 'c'}
    },
    {  # wrong 1st key
        'input_dict': {'a': {'b': 'c'}},
        'key_list': ['x', 'b'],
        'expected_data': None
    },
    {  # wrong 2nd key
        'input_dict': {'a': {'b': 'c'}},
        'key_list': ['a', 'x'],
        'expected_data': None
    },
    {  # too many keys
        'input_dict': {'a': {'b': 'c'}},
        'key_list': ['a', 'b', 'c'],
        'expected_data': None
    },
    {  # no keys
        'input_dict': {'a': {'b': 'c'}},
        'key_list': [],
        'expected_data': {'a': {'b': 'c'}}
    },
])
def test_nested_dict_get(data):
    assert data['expected_data'] == nested_get(data['input_dict'], data['key_list'])


@pytest.mark.parametrize('data', [
    {  # normal use case
        'input': [(1, 'a'), (2, 'b'), (3, 'c')],
        'output': ([1, 2, 3], ['a', 'b', 'c'])
    },
    {  # empty
        'input': [],
        'output': ([], [])
    },
    {  # length 3
        'input': [(1, 'a', 1.0), (2, 'b', 2.0), (3, 'c', 3.0)],
        'output': ([1, 2, 3], ['a', 'b', 'c'], [1.0, 2.0, 3.0])
    },
    {  # length 1
        'input': [(1, 'a')],
        'output': ([1], ['a'])
    },
])
def test_split_data_using_transpose(data):
    assert data['output'] == split_data_using_transpose(data['input'])
