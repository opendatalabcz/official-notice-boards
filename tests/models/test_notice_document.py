import json

import pytest

from src.models import NoticeDocument


# def test_extract_from_dict():
#     data = {'url': 'https://www.obec.cz/uredni-deska/doc_1.pdf'}
#     notice_document = NoticeDocument.extract_from_dict(data)
#     assert notice_document.download_url == 'https://www.obec.cz/uredni-deska/doc_1.pdf'


@pytest.mark.parametrize('data', [
    {  # only basic url
        'input_data':
            {
                'url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
            },
        'expected_data':
            {
                'name': None,
                'download_url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
            }
    },
    {  # url + name
        'input_data':
            {
                'název': {'cs': 'doc_1.pdf'},
                'url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
                'type': 'special secret document type'
            },
        'expected_data':
            {
                'name': 'doc_1.pdf',
                'download_url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
            }
    },
    {  # empty json dict
        'input_data':
            {},
        'expected_data':
            {
                'name': None,
                'download_url': None,
            }
    },
    {  # wrong url name
        'input_data':
            {
                'download_url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
            },
        'expected_data':
            {
                'name': None,
                'download_url': None,
            }
    },
    {  # extra data
        'input_data':
            {
                'název': {'cs': 'doc_1.pdf'},
                'url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
                'type': 'special secret document type'
            },
        'expected_data':
            {
                'name': 'doc_1.pdf',
                'download_url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
            }
    },
    {  # wrong name format
        'input_data':
            {
                'name_wrong_format': {'language': 'cs', 'name': 'doc_1.pdf'},
                'url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
                'type': 'special secret document type'
            },
        'expected_data':
            {
                'name': None,
                'download_url': 'https://www.obec.cz/uredni-deska/doc_1.pdf',
            }
    },
])
def test_extract_from_dict(data):
    # with pytest.raises(Exception):
    # assert False
    notice_document = NoticeDocument.extract_from_dict(data.get('input_data', {}))
    for key, value in data.get('expected_data', {}).items():
        assert notice_document.__dict__[key] == value


@pytest.mark.parametrize('data', [
    None,
    [],
    json.dumps({'url': 'https://www.obec.cz/uredni-deska/doc_1.pdf'}),
    "<url>https://www.obec.cz/uredni-deska/doc_1.pdf</url>"
])
def test_extract_from_dict_fail(data):
    with pytest.raises(AttributeError):
        NoticeDocument.extract_from_dict(data)
