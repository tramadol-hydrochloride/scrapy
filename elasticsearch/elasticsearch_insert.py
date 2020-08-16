import sys
import hashlib
import json

from elasticsearch import Elasticsearch


# Create Elasticsearch client
es = Elasticsearch(['localhost:9200'])

body = {
    'settings': {
        'analysis': {
            'analyzer': {
                'kuromoji_analyzer': {
                    'tokenizer': 'kuromoji_tokenizer'
                }
            }
        }
    },
    'mappings': {
        'page': {
            '_all': {'analyzer': 'kuromoji_analyzer'},
            'properties': {
                'url': {'type': 'string'},
                'title': {'type': 'string', 'analyzer': 'kuromoji_analyzer'},
                'content': {'type': 'string', 'analyzer': 'kuromoji_analyzer'}
            }
        }
    }
}

result = es.indices.create(index='pages', ignore=400, body=body)

print(result)


# Read JSON Lines file line by line
with open(sys.argv[1]) as f:
    for line in f:
        page = json.loads(line)

        doc_id = hashlib.sha1(page['url'].encode('utf-8')).hexdigest()
        result = es.index(index='pages', doc_type='page', id=doc_id, body=page)

        print(result)
