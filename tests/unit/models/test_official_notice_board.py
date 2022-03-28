import pytest

from app.models import OfficialNoticeBoard

@pytest.mark.parametrize('data', [
    {  # all present
        'input_data':
            {
                'ico':
                    {'type': 'literal', 'value': '00123456'},
                'office_name':
                    {'type': 'literal', 'xml:lang': 'cs', 'value': 'This is an office name'},
                'download_link':
                    {'type': 'uri', 'value': 'https://www.uri.download_link.cz/foo'},
                'access_link':
                    {'type': 'uri', 'value': 'https://www.uri.access_link.cz/bar'}
            },
        'expected_data':
            {
                'ico': '00123456',
                'office_name': 'This is an office name',
                'download_url': 'https://www.uri.download_link.cz/foo',
                'office_name_missing': None,
                'ico_missing': None,
                'download_url_missing': None,
                'download_url_unreachable': None,
                'attempted_download': None,
                'notices_missing': None,
                'modify SPARQL': None,
            }
    },
    {  # access link missing
        'input_data':
            {
                'ico':
                    {'type': 'literal', 'value': '00123456'},
                'office_name':
                    {'type': 'literal', 'xml:lang': 'cs', 'value': 'This is an office name'},
                'download_link':
                    {'type': 'uri', 'value': 'https://www.uri.download_link.cz/foo'},
            },
        'expected_data':
            {
                'ico': '00123456',
                'office_name': 'This is an office name',
                'download_url': 'https://www.uri.download_link.cz/foo',

                'office_name_missing': None,
                'ico_missing': None,
                'download_url_missing': None,
                'download_url_unreachable': None,
                'attempted_download': None,
                'notices_missing': None,
                'modify SPARQL': None,
            }
    },
    {  # download link missing
        'input_data':
            {
                'ico':
                    {'type': 'literal', 'value': '00123456'},
                'office_name':
                    {'type': 'literal', 'xml:lang': 'cs', 'value': 'This is an office name'},
                'access_link':
                    {'type': 'uri', 'value': 'https://www.uri.access_link.cz/bar'}
            },
        'expected_data':
            {
                'ico': '00123456',
                'office_name': 'This is an office name',
                'download_url': 'https://www.uri.access_link.cz/bar',

                'office_name_missing': None,
                'ico_missing': None,
                'download_url_missing': None,
                'download_url_unreachable': None,
                'attempted_download': None,
                'notices_missing': None,
                'modify SPARQL': None,
            }
    },
    {  # both access link and download link missing
        'input_data':
            {
                'ico':
                    {'type': 'literal', 'value': '00123456'},
                'office_name':
                    {'type': 'literal', 'xml:lang': 'cs', 'value': 'This is an office name'},
            },
        'expected_data':
            {
                'ico': '00123456',
                'office_name': 'This is an office name',
                'download_url': None,

                'office_name_missing': None,
                'ico_missing': None,
                'download_url_missing': True,
                'download_url_unreachable': None,
                'attempted_download': None,
                'notices_missing': None,
                'modify SPARQL': None,
            }
    },
    {  # ico missing
        'input_data':
            {
                'office_name':
                    {'type': 'literal', 'xml:lang': 'cs', 'value': 'This is an office name'},
                'download_link':
                    {'type': 'uri', 'value': 'https://www.uri.download_link.cz/foo'},
                'access_link':
                    {'type': 'uri', 'value': 'https://www.uri.access_link.cz/bar'}
            },
        'expected_data':
            {
                'ico': None,
                'office_name': 'This is an office name',
                'download_url': 'https://www.uri.download_link.cz/foo',

                'office_name_missing': None,
                'ico_missing': True,
                'download_url_missing': None,
                'download_url_unreachable': None,
                'attempted_download': None,
                'notices_missing': None,
                'modify SPARQL': None,
            }
    },
    {  # office name missing
        'input_data':
            {
                'ico':
                    {'type': 'literal', 'value': '00123456'},
                'download_link':
                    {'type': 'uri', 'value': 'https://www.uri.download_link.cz/foo'},
                'access_link':
                    {'type': 'uri', 'value': 'https://www.uri.access_link.cz/bar'}
            },
        'expected_data':
            {
                'ico': '00123456',
                'office_name': None,
                'download_url': 'https://www.uri.download_link.cz/foo',

                'office_name_missing': True,
                'ico_missing': None,
                'download_url_missing': None,
                'download_url_unreachable': None,
                'attempted_download': None,
                'notices_missing': None,
                'modify SPARQL': None,
            }
    },
    {  # all missing
        'input_data':
            {},
        'expected_data':
            {
                'ico': None,
                'office_name': None,
                'download_url': None,

                'office_name_missing': True,
                'ico_missing': True,
                'download_url_missing': True,
                'download_url_unreachable': None,
                'attempted_download': None,
                'notices_missing': None,
                'modify SPARQL': None,
            }
    },
    {  # access link missing, donwload link incorrect
        'input_data':
            {
                'ico':
                    {'type': 'literal', 'value': '00123456'},
                'office_name':
                    {'type': 'literal', 'xml:lang': 'cs', 'value': 'This is an office name'},
                'download_link':
                    {'type': 'uri', 'link_wrong_key': 'https://www.uri.download_link.cz/foo'},
            },
        'expected_data':
            {
                'ico': '00123456',
                'office_name': 'This is an office name',
                'download_url': None,

                'office_name_missing': None,
                'ico_missing': None,
                'download_url_missing': True,
                'download_url_unreachable': None,
                'attempted_download': None,
                'notices_missing': None,
                'modify SPARQL': None,
            }
    },
])
def test_extract_from_dict(data):
    notice_document = OfficialNoticeBoard.extract_from_dict(data.get('input_data', {}))
    for key, value in data.get('expected_data', {}).items():
        assert notice_document.__dict__.get(key) == value
