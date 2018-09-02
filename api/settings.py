"""Settings."""
import os
from os.path import join, dirname, abspath

from elasticsearch import Elasticsearch


def get_client():
    """Get Elasticsearch client."""
    return Elasticsearch(hosts=[
        '{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'.format(**os.environ)]
    )


STATIC_PATH = join(dirname(abspath(__file__)), 'static')
