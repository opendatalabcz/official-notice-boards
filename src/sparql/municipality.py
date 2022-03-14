from typing import Any

import requests

from src.sparql.endpoint import Endpoint
from src.sparql.query import run_query

_MUNICIPALITY_LIST_DESCRIPTION = "Číselník obcí ČR."
_MUNICIPALITY_PART_LIST_DESCRIPTION = "Číselník městských obvodů a městských částí"

_GET_DOWNLOAD_LIST_QUERY = \
    """
    SELECT ?download_url WHERE
    {{
        ?municipalities_list dct:description  "{description}"@cs;
                             dcat:distribution ?distribution.
        ?distribution dct:format ?format;
                      dcat:downloadURL ?download_url.
        ?format dc:identifier "JSON".
    }}
    """


def _fetch_list_url(is_part: bool) -> str:
    description = _MUNICIPALITY_PART_LIST_DESCRIPTION if is_part else _MUNICIPALITY_LIST_DESCRIPTION
    query = _GET_DOWNLOAD_LIST_QUERY.format(description=description)
    result = run_query(query, Endpoint.DATA_GOV)
    url = result['results']['bindings'][0]['download_url']['value']
    return url


def fetch_municipality_list(is_part: bool) -> list[dict[Any, Any]]:
    url = _fetch_list_url(is_part)
    return requests.get(url).json()['polozky']
