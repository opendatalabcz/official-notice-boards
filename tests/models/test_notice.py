from datetime import datetime

import pytest

from src.models import Notice


@pytest.mark.parametrize("data", [
    {  # basic date
        "input_data":
            {
                "datum": "2021-12-30"
            },
        "expected_datetime": datetime(year=2021, month=12, day=30)
    },
    {  # wrong format - unsupported wrong date key
        'input_data':
            {
                "datum_wrong_format": "2021-12-30"
            },
        'expected_datetime': None
    },
    {  # no date
        'input_data': {},
        'expected_datetime': None
    },
    {  # wrong format - supported wrong date key
        "input_data":
            {
                "datum_a_čas": "2021-12-30"
            },
        "expected_datetime": datetime(year=2021, month=12, day=30)
    },
    {  # wrong format - supported wrong date key
        "input_data":
            {
                "Časový okamžik": "2021-12-30"
            },
        "expected_datetime": datetime(year=2021, month=12, day=30)
    },
    {  # extra data
        "input_data":
            {
                "foo" : "bar",
                "datum": "2021-12-30"
            },
        "expected_datetime": datetime(year=2021, month=12, day=30)
    },
])
def test_extract_datetime_from_dict(data):
    assert data['expected_datetime'] == Notice._extract_datetime_from_dict(data['input_data'])


@pytest.mark.parametrize("data", [
    {"datum": "2021-30-12"},  # swapped date and month
    {"datum": "12-30-2021"},  # year first
    {"datum": "2021/12/30"},  # swapped date and month
    {"datum": "2021.12.30"},  # swapped date and month
    {"datum": "20211230"},  # swapped date and month
    # TODO add more tests; non ISO formats, ...
])
def test_extract_datetime_from_dict_exception(data):
    with pytest.raises(Exception):
        Notice._extract_datetime_from_dict(data)
