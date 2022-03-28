# get list of official notice boards

# kinda useless
select_official_notice_boards_w_names = \
    'SELECT ?urad ?datova_sada WHERE { ' \
    '?datova_sada dct:conformsTo  ofn:úřední-desky\/2021-07-20\/ ;' \
    ' dct:publisher ?urad .' \
    '}'

# useless
select_official_notice_boards_w_office_link_with_ruian = \
"""
SELECT ?datova_sada ?spatial WHERE {
?datova_sada dct:conformsTo ofn:úřední-desky\/2021-07-20\/ ;
                         dct:spatial ?spatial
}
"""

# TODO use
select_official_notice_boards_w_ico = \
"""
SELECT ?datova_sada ?name ?ico WHERE {
?datova_sada dct:conformsTo ofn:úřední-desky\/2021-07-20\/ ;
                         dct:publisher ?publisher.
OPTIONAL {
?publisher l-sgov-sb-111-2009-pojem:má-název-orgánu-veřejné-moci ?name ;
                   l-sgov-sb-111-2009-pojem:má-identifikátor-orgánu-veřejné-moci ?ico

}
}
"""

# TODO use
select_official_notice_boards_w_board_download_links = \
"""
    SELECT ?publisher ?datova_sada ?distribution ?download_link WHERE {
    ?datova_sada dct:conformsTo ofn:úřední-desky\/2021-07-20\/ ;
                             dcat:distribution ?distribution;
                             dct:publisher ?publisher .
    ?distribution  dcat:downloadURL ?download_link .
    }
"""


fasdf = \
"""
SELECT ?datova_sada ?office_name ?download_link ?access_link WHERE {
    ?datova_sada dct:conformsTo ofn:úřední-desky\/2021-07-20\/ ;
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

# different queries to count official notice boards
count_official_notice_board_based_on_set_spec = \
    'SELECT (COUNT (?datova_sada)) WHERE { ?datova_sada dct:conformsTo  ofn:úřední-desky\/2021-07-20\/ .}'
count_official_notice_board_based_on_latest_spec = \
    'SELECT (COUNT (?datova_sada)) WHERE { ?datova_sada dct:conformsTo ofn:úřední-desky\/ .}'
count_official_notice_board_based_on_keyword_cs = \
    'SELECT (COUNT (?datova_sada)) WHERE { ?datova_sada dcat:keyword "úřední deska"@cs .}'
count_official_notice_board_based_on_keyword_en = \
    'SELECT (COUNT (?datova_sada)) WHERE { ?datova_sada dcat:keyword "bulletin board"@en .}'


# get_download_links_of_municipality_parts_list = \
# """
# SELECT ?download_url WHERE {
# ?municipalities_list dct:description  "Číselník městských obvodů a městských částí"@cs;
#                      dcat:distribution ?distribution.
# ?distribution dct:format ?format;
#               dcat:downloadURL ?download_url.
# ?format dc:identifier "JSON".
# }
# """
#
#
# get_download_links_of_municipalities_list = \
# """
# SELECT ?download_url WHERE {
# ?municipalities_list dct:description  "Číselník obcí ČR."@cs;
#                      dcat:distribution ?distribution.
# ?distribution dct:format ?format;
#               dcat:downloadURL ?download_url.
# ?format dc:identifier "JSON".
# }
# """

# useless
def search_notice_board_by_municipality_ruian(ruian: str) -> str:
    return """
    SELECT ?datova_sada ?publisher WHERE {
    ?datova_sada dct:conformsTo ofn:úřední-desky\/2021-07-20\/ ;
                             dct:publisher ?publisher ;
                             dct:spatial <https://linked.cuzk.cz/resource/ruian/obec/{ruian}}>
    }
    """.format(ruian=ruian)

# def run_query(query: str) -> dict[Any, Any]:
#     sparql = SPARQLWrapper(DATA_GOV_SPARQL_ENDPOINT)
#     sparql.setReturnFormat(JSON)
#
#     sparql_query = _PREFIXES + query  # <==== change here
#     sparql.setQuery(sparql_query)
#     try:
#         ret = sparql.query()
#         return ret.convert()
#     except Exception as e:
#         print("Query failed")
#         print(e.with_traceback())
#     return {'status': 'failed'}


# def get_municipalities_list() -> str:  # TODO move
#     query_result = run_query(get_download_links_of_municipalities_list, Endpoint.DATA_GOV)
#     url = query_result['results']['bindings'][0]['download_url']['value']
#     return requests.get(url).json()['polozky']
#
#
# def get_municipality_parts_list() -> str:
#     query_result = run_query(get_download_links_of_municipality_parts_list, Endpoint.DATA_GOV)
#     url = query_result['results']['bindings'][0]['download_url']['value']
#     return requests.get(url).json()['polozky']
#

def main():
    # ret = sparql.query()
    # print(f"{ret.response.read().decode('utf-8')=}")
    # print(f"{ret.convert()=}")
    pass


if __name__ == '__main__':
    main()
