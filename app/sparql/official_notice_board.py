from json import JSONDecodeError
from typing import Any

from app.sparql.endpoint import Endpoint
from app.sparql.query import run_query
from app.utils import requests_wrapper

_GET_BOARDS_QUERY = \
    """
    SELECT ?datova_sada ?ico ?title ?office_name ?download_link ?access_link WHERE {
        ?datova_sada dct:conformsTo ofn:úřední-desky\\/2021-07-20\\/ ;
                                    dcat:distribution ?distribution;
                                    dct:publisher ?publisher ;
                                    dct:title ?title.
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
        FILTER(lang(?title) = 'cs')
    }
    """


def fetch_boards_data() -> list[dict[Any, Any]]:
    query_result = run_query(_GET_BOARDS_QUERY, Endpoint.DATA_GOV)
    return query_result['results']['bindings']


def fetch_board(url: str) -> list[dict[Any, Any]] | None:
    response = requests_wrapper.get(url)
    if response is None:
        return None

    try:
        json_response = response.json()
    except JSONDecodeError:
        return None

    if isinstance(json_response, list):
        json_response = json_response[0]

    return json_response.get('informace')
