from app.sparql.endpoint import Endpoint
from app.sparql.query import run_query
from app.utils.random_stuff import nested_get

# _GET_MAPPER_QUERY = \
# SELECT
# DISTINCT ?city ?label ?ruian ?ico ?website_url  # ?email
# WHERE
# {
#     {
# ?city
# wdt: P7577 ?ruian;
# rdfs: label ?label.
#     OPTIONAL
# {
# ?city
# wdt: P4156 ?ico.
# }
# OPTIONAL
# {
# ?city
# wdt: P856 ?website_url
# }
# OPTIONAL
# {
#     #  ?city wdt:P968 ?email
# }
# }
# UNION
# {
# ?city
# wdt: P31
# wd: Q5153359;
# rdfs: label ?label;
# wdt: P4156 ?ico;
# wdt: P7606 ?ruian.
#     OPTIONAL
# {
# ?city
# wdt: P856 ?website_url
# }
# OPTIONAL
# {
#     #   ?city wdt:P968 ?email
# }
# }
# FILTER(lang(?label) = 'cs')
# }

#     """

MAP_RUIAN_2_ICO_QUERY = \
    """
    SELECT DISTINCT ?city ?ruian ?ico
    WHERE
    {
      {
        ?city wdt:P7577 ?ruian .
        OPTIONAL
        {
          ?city wdt:P4156 ?ico .
        }
      }
      UNION
      {
        ?city wdt:P31 wd:Q5153359 ;
              wdt:P4156 ?ico ;
              wdt:P7606 ?ruian .
      }
    }
    """

EXTENDED_POWER_MUNICIPALITIES_QUERY = \
    """
    SELECT DISTINCT ?city ?ruian
    {
        ?city wdt:P31 wd:Q7819319 ;
              wdt:P7606 ?ruian
    }
    """


def fetch_ruian_2_ico_mapper():
    """Iterator that return tuples of (ruian, ico)"""
    query_result = run_query(MAP_RUIAN_2_ICO_QUERY, Endpoint.WIKIDATA)['results']['bindings']

    for record in query_result:
        yield (
            nested_get(record, ['ruian', 'value']),
            nested_get(record, ['ico', 'value'])
        )


def fetch_extended_power_municipalities_list():
    query_result = run_query(EXTENDED_POWER_MUNICIPALITIES_QUERY, Endpoint.WIKIDATA)['results']['bindings']

    for record in query_result:
        yield nested_get(record, ['ruian', 'value'])
