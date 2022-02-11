import logging
from typing import Any

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import SPARQLWrapperException

from src.utils.sparql.endpoints import Endpoint

_PREFIXES = """
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
"""


def run_query(query: str, endpoint: Endpoint) -> dict[Any, Any]:
    sparql = SPARQLWrapper(endpoint.value)
    sparql.setReturnFormat(JSON)

    sparql.setQuery(_PREFIXES + query)
    try:
        ret = sparql.query()
        return ret.convert()
    except SPARQLWrapperException:
        logging.info("Sparql Query failed: %s", query)
    return {'status': 'failed'}
