from datetime import datetime

import pytest

from app import db
from app.models import Notice


@pytest.mark.parametrize("data", [
    {  # basic date
        "input_data":
            {
                "datum": "2021-12-30"
            },
        "expected_data": (datetime(year=2021, month=12, day=30), False)
    },
    {  # wrong format - unsupported wrong date key
        'input_data':
            {
                "datum_wrong_format": "2021-12-30"
            },
        'expected_data': (None, True)
    },
    {  # no date
        'input_data': {},
        'expected_data': (None, True)
    },
    {  # wrong format - supported wrong date key
        "input_data":
            {
                "datum_a_čas": "2021-12-30"
            },
        "expected_data": (datetime(year=2021, month=12, day=30), False)
    },
    {  # wrong format - supported wrong date key
        "input_data":
            {
                "Časový okamžik": "2021-12-30"
            },
        "expected_data": (datetime(year=2021, month=12, day=30), True)
    },
    {  # extra data
        "input_data":
            {
                "foo" : "bar",
                "datum": "2021-12-30"
            },
        "expected_data": (datetime(year=2021, month=12, day=30), False)
    },
    {  # with leading zeros
        "input_data":
            {
                "datum": "2021-01-01"
            },
        "expected_data": (datetime(year=2021, month=1, day=1), False)
    },
])
def test_extract_datetime_from_dict(data):
    assert data['expected_data'] == Notice._extract_datetime_from_dict(data['input_data'])


@pytest.mark.parametrize("data", [
    {"datum": "2021-30-12"},  # swapped date and month
    {"datum": "12-30-2021"},  # year first
    {"datum": "2021/12/30"},  # swapped date and month
    {"datum": "2021.12.30"},  # swapped date and month
    {"datum": "20211230"},  # swapped date and month
    {"datum": "2021-1-1"},  # no leading zeros
    # TODO add more tests; non ISO formats, ..., especially with time
])
def test_extract_datetime_from_dict_exception(data):
    with pytest.raises(Exception):
        Notice._extract_datetime_from_dict(data)


# For some keys in expected_data, their value is None, because the instance
# has not been added to DB, so the default value has not yet been set
@pytest.mark.parametrize('data', [
    {  # basic
        'input_data':
            {
                # "typ": [
                #     "Type1",
                #     "TypeB"
                # ],
                "url": "https://www.url.foo.cz",
                "iri": "https://www.iri.foo.cz",
                "název": {
                    "cs": "This is a name"
                },
                "popis": {
                    "cs": "This is a description. Lorem ipsum, and stuff like that you know"
                },
                "číslo_jednací": "ref 2022/01 smth 5",
                "vyvěšení": {
                    "typ": "Časový okamžik",
                    "datum": "2021-12-30"
                },
                "relevantní_do": {
                    "typ": "Časový okamžik",
                    "datum": "2020-11-29"
                    # "nespecifikovaný": True
                }
            },
        'expected_data':
            {
                "url": "https://www.url.foo.cz",
                "iri": "https://www.iri.foo.cz",
                "name": "This is a name",
                "description": "This is a description. Lorem ipsum, and stuff like that you know",
                "reference_number": "ref 2022/01 smth 5",
                "post_date": datetime(year=2021, month=12, day=30),
                "relevant_until_date": datetime(year=2020, month=11, day=29),

                "url_missing": False,
                "iri_missing": False,
                "post_date_wrong_format": False,
                "relevant_until_date_wrong_format": False,
                "documents_missing": True,
                "documents_wrong_format": None,
            },
        'document_count': 0
    },
    {  # missing data
        'input_data':
            {},
        'expected_data':
            {
                "url": None,
                "iri": None,
                "name": None,
                "post_date": None,
                "relevant_until_date": None,

                "url_missing": True,
                "iri_missing": True,
                "post_date_wrong_format": True,
                "relevant_until_date_wrong_format": True,
                "documents_missing": True,
                "documents_wrong_format": None,
            },
        'document_count': 0
    },
    {  # unspecified date, but correctly with specs
        'input_data':
            {
                "url": "https://www.url.foo.cz",
                "iri": "https://www.iri.foo.cz",
                "název": {
                    "cs": "This is a name"
                },
                "vyvěšení": {
                    "typ": "Časový okamžik",
                    "datum": "2021-12-30"
                },
                "relevantní_do": {
                    "typ": "Časový okamžik",
                    "nespecifikovaný": True
                }
            },
        'expected_data':
            {
                "url": "https://www.url.foo.cz",
                "iri": "https://www.iri.foo.cz",
                "name": "This is a name",
                "post_date": datetime(year=2021, month=12, day=30),
                "relevant_until_date": None,

                "url_missing": False,
                "iri_missing": False,
                "post_date_wrong_format": False,
                "relevant_until_date_wrong_format": False,
                "documents_missing": True,
                "documents_wrong_format": None,
            },
        'document_count': 0
    },
    {  # 1 document
        'input_data':
            {
                "url": "https://www.url.foo.cz",
                "iri": "https://www.iri.foo.cz",
                "název": {
                    "cs": "This is a name"
                },
                "vyvěšení": {
                    "typ": "Časový okamžik",
                    "datum": "2021-12-30"
                },
                "relevantní_do": {
                    "typ": "Časový okamžik",
                    "datum": "2020-11-29"
                },
                "dokument": [
                    {
                        "typ": "Type1A",
                        "název": {
                            "cs": "file_id_1.pdf"
                        },
                        "url": "https://www.document_url.cz/file.pdf"
                    }
                ],
                # "odkaz": [],
                # "kategorie": "Jiná oznámení"
            },
        'expected_data':
            {
                "url": "https://www.url.foo.cz",
                "iri": "https://www.iri.foo.cz",
                "name": "This is a name",
                "post_date": datetime(year=2021, month=12, day=30),
                "relevant_until_date": datetime(year=2020, month=11, day=29),

                "url_missing": False,
                "iri_missing": False,
                "post_date_wrong_format": False,
                "relevant_until_date_wrong_format": False,
                "documents_missing": None,
                "documents_wrong_format": None,
            },
        'document_count': 1
    },
    {  # more documents
        'input_data':
            {
                "url": "https://www.url.foo.cz",
                "iri": "https://www.iri.foo.cz",
                "název": {
                    "cs": "This is a name"
                },
                "vyvěšení": {
                    "typ": "Časový okamžik",
                    "datum": "2021-12-30"
                },
                "relevantní_do": {
                    "typ": "Časový okamžik",
                    "datum": "2020-11-29"
                },
                # "vyvěšení": {
                #     "typ": "Časový okamžik",
                #     "datum": "2022-03-15T14:01:00+01:00"
                # },
                # "relevantní_do": {
                #     "typ": "Časový okamžik",
                #     "datum": "2022-04-19T23:00:00+01:00"
                # },
                "dokument": [
                    {
                        "typ": "Type1A", "název": { "cs": "file_id_1.pdf"},
                        "url": "https://www.document1_url.cz/file1.pdf"
                    },
                    {
                        "typ": "Type2B", "název": {"cs": "file_id_2.pdf"},
                        "url": "https://www.document2_url.cz/file2.pdf"
                    },
                    {
                        "typ": "Type3B", "název": {"cs": "file_id_3.pdf"},
                        "url": "https://www.document3_url.cz/file3.pdf"
                    },
                ],
                # "odkaz": [],
                # "kategorie": "Jiná oznámení"
            },
        'expected_data':
            {
                "url": "https://www.url.foo.cz",
                "iri": "https://www.iri.foo.cz",
                "name": "This is a name",
                "post_date": datetime(year=2021, month=12, day=30),
                "relevant_until_date": datetime(year=2020, month=11, day=29),

                "url_missing": False,
                "iri_missing": False,
                "post_date_wrong_format": False,
                "relevant_until_date_wrong_format": False,
                "documents_missing": None,
                "documents_wrong_format": None,
            },
        'document_count': 3
    },
])
def test_extract_from_dict(data):
    # with pytest.raises(Exception):
    # assert False
    notice = Notice.extract_from_dict(data['input_data'])
    # db.session.add(notice)
    for key, value in data['expected_data'].items():
        assert notice.__dict__.get(key) == value
        assert len(notice.documents) == data.get('document_count')
