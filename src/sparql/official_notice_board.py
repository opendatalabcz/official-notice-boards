from json import JSONDecodeError
from typing import Any, Optional

import requests
from requests.exceptions import SSLError

from src.models.official_notice_board import OfficialNoticeBoard
from src.sparql.endpoint import Endpoint
from src.sparql.query import run_query, _AGENT, _AGENT_DICT
from src.utils import requests_wrapper

_GET_BOARDS_QUERY = \
    """
    SELECT ?datova_sada ?ico ?office_name ?download_link ?access_link WHERE {
        ?datova_sada dct:conformsTo ofn:úřední-desky\\/2021-07-20\\/ ;
                                    dcat:distribution ?distribution;
                                    dct:publisher ?publisher .
        OPTIONAL
        {
            ?distribution  dcat:downloadURL ?download_link .
        }
        OPTIONAL
        {
            ?distribution  dcat:accessURL ?access_link .
        }
        OPTIONAL
        {
            ?publisher l-sgov-sb-111-2009-pojem:má-název-orgánu-veřejné-moci ?office_name ;
                       l-sgov-sb-111-2009-pojem:má-identifikátor-orgánu-veřejné-moci ?ico .
        }
    }
    """


def fetch_boards_data() -> list[dict[Any, Any]]:
    query_result = run_query(_GET_BOARDS_QUERY, Endpoint.DATA_GOV)
    return query_result['results']['bindings']


def fetch_board(url: str) -> list[dict[Any, Any]]:
    response = requests_wrapper.get(url)
    if response is None:
        return []

    try:
        json_response = response.json()
    except JSONDecodeError:
        return []

    # prob only because of https://opendata.mvcr.cz/api/boards?type=hzs
    if isinstance(json_response, list):
        json_response = json_response[0]

    return json_response.get('informace', [])
