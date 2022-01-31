from SPARQLWrapper import SPARQLWrapper, JSON

DATA_GOV_SPARQL_ENDPOINT = "https://data.gov.cz/sparql/"

_PREFIXES = 'PREFIX dcat: <http://www.w3.org/ns/dcat#> \
             PREFIX dct: <http://purl.org/dc/terms/>   \
             PREFIX foaf: <http://xmlns.com/foaf/0.1/> \
             PREFIX ofn: <https://ofn.gov.cz/>'

# get list of official notice boards
select_official_notice_boards = \
    'SELECT ?datova_sada WHERE { ?datova_sada dct:conformsTo  ofn:úřední-desky\/2021-07-20\/ .}'

select_official_notice_boards_w_names = \
    'SELECT ?urad ?datova_sada WHERE { ' \
    '?datova_sada dct:conformsTo  ofn:úřední-desky\/2021-07-20\/ ;' \
    ' dct:publisher ?urad .' \
    '}'

# different queries to count official notice boards
count_official_notice_board_based_on_set_spec = \
    'SELECT (COUNT (?datova_sada)) WHERE { ?datova_sada dct:conformsTo  ofn:úřední-desky\/2021-07-20\/ .}'
count_official_notice_board_based_on_latest_spec = \
    'SELECT (COUNT (?datova_sada)) WHERE { ?datova_sada dct:conformsTo ofn:úřední-desky\/ .}'
count_official_notice_board_based_on_keyword_cs = \
    'SELECT (COUNT (?datova_sada)) WHERE { ?datova_sada dcat:keyword "úřední deska"@cs .}'
count_official_notice_board_based_on_keyword_en = \
    'SELECT (COUNT (?datova_sada)) WHERE { ?datova_sada dcat:keyword "bulletin board"@en .}'

# get list of municipality parts
get_municipality_parts_list = \
    'SELECT ?parts_list WHERE { ?parts_list dct:description  "Číselník městských obvodů a městských částí"@cs .}'

# get list of municipalities
get_municipalities_list = \
    'SELECT ?municipalities_list WHERE { ?municipalities_list dct:description  "Číselník obcí ČR."@cs .}'


def main():

    sparql = SPARQLWrapper(DATA_GOV_SPARQL_ENDPOINT)
    # sparql.setReturnFormat(JSON)

    sparql_query = _PREFIXES + select_official_notice_boards_w_names  # <==== change here
    sparql.setQuery(sparql_query)

    try:
        ret = sparql.query()
        print(str(ret.response.read().decode('utf-8')))
    except Exception as e:
        print("Query failed")
        print(e.with_traceback())


if __name__ == '__main__':
    main()
