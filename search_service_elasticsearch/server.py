from elasticsearch import Elasticsearch
from bottle import route, run, request, template


es = Elasticsearch(['localhost:9200'])


@route('/')
def index():
    """ Process request at '/'  """

    # Get query parameter (?q='')
    query = request.query.q
    pages = search_pages(query) if query else []

    # Pass query and pages to the Bottle's template (search.tpl)
    # Return rendering results as response body
    return template('search', query=query, pages=pages)


def search_pages(query):
    """ Search webpage with query from Elasticsearch """

    result = es.search(index='pages', doc_type='page', body={
        'query': {
            'simple_query_string': {
                'query': query,
                'fields': ['title^5', 'content'],
                'default_operator': 'and'
            }
        },
        'highlight': {
            'fields': {
                'content': {
                    'fragment_size': 150,
                    'number_of_fragments': 1,
                    'no_match_size': 150
                }
            }
        }
    })

    # Return webpage list
    return result['hits']['hits']


if __name__=='__main__':
    run(host='0.0.0.0', port=8000, debug=True, reloader=True)
