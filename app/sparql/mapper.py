from app.sparql.endpoint import Endpoint
from app.sparql.query import run_query

# _GET_MAPPER_QUERY = \
#     """
#     SELECT DISTINCT ?city ?ruian ?ico ?location
#     WHERE
#     {
#       {
#         ?city wdt:P7577 ?ruian ;
#               wdt:P625 ?location .
#         OPTIONAL
#         {
#           ?city wdt:P4156 ?ico .
#         }
#       }
#       UNION
#       {
#         ?city wdt:P31 wd:Q5153359 ;
#               wdt:P4156 ?ico ;
#               wdt:P7606 ?ruian ;
#               wdt:P625 ?location .
#       }
#     }
#     """

_GET_MAPPER_QUERY = \
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

def fetch_mapper_data():
    query_result = run_query(_GET_MAPPER_QUERY, Endpoint.WIKIDATA)
    return query_result['results']['bindings']
