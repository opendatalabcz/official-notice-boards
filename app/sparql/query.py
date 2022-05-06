import logging
from typing import Any

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import SPARQLWrapperException
from flask import current_app

from app.sparql.endpoint import Endpoint

_PREFIXES = \
    """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX ofn: <https://ofn.gov.cz/>
    PREFIX l-sgov-sb-111-2009-pojem: <https://slovník.gov.cz/legislativní/sbírka/111/2009/pojem/>
    """

# agent has to be set with wikidata endpoint, because it might return HTTP 403 error
_AGENT = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " \
         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"


def run_query(query: str, endpoint: Endpoint) -> dict[Any, Any]:
    sparql = SPARQLWrapper(endpoint.value, agent=_AGENT)
    sparql.setReturnFormat(JSON)

    sparql.setQuery(_PREFIXES + query)
    try:
        current_app.logger.info("Sending SPARQL query: %s", query)
        ret = sparql.query()
        return ret.convert()
    except SPARQLWrapperException:
        current_app.logger.warning("Sparql Query failed: %s", query)
    return {'status': 'failed'}
