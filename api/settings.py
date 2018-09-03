"""Settings."""
import os
from os.path import join, dirname, abspath

from elasticsearch import Elasticsearch


def get_client():
    """Get Elasticsearch client."""
    return Elasticsearch(hosts=[
        '{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'.format(**os.environ)]
    )


# falcon-swagger-ui
STATIC_PATH = join(dirname(abspath(__file__)), 'static')
SWAGGERUI_URL = '/api'
SCHEMA_URL = 'http://140.112.147.121:9000/static/spec.json'
PAGE_TITLE = 'PTT Engine API'
FAVICON_URL = (
    'http://lopen.linguistics.ntu.edu.tw/static_pttcorp/images/PTTCorp.ico')
