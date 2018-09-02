"""Settings."""
import os

from elasticsearch import Elasticsearch


def get_client():
    """Get Elasticsearch client."""
    return Elasticsearch(hosts=[
        '{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'.format(**os.environ)]
    )
