from enum import Enum


class Endpoint(Enum):
    WIKIDATA = "https://query.wikidata.org/sparql"
    DATA_GOV = "https://data.gov.cz/sparql/"
