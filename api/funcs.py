"""Core functions."""
from datetime import datetime

from elasticsearch_dsl import (
    Search,
    Q,
)

from settings import get_client


client = get_client()


def query(word: str,
          page: int,
          size: int,
          post_type: int,
          boards: list,
          sort: str,
          order: str,
          start: datetime=None,
          end: datetime=None) -> dict:
    """Query word."""
    s = Search(using=client, index='ptt')
    s.query = Q(
        'bool',
        must=[
            Q('match', content=word),
            Q('match', post_type=post_type),
        ],
        should=[
            Q('match', board=board)
            for board
            in boards
        ],
        minimum_should_match=1,
    )

    # sort and order
    s = s.sort({sort: {'order': order}})

    # filter date range
    s = s.filter('range', published={'gte': start, 'lte': end})

    total = s.count()
    left_bound = page * size
    right_bound = left_bound + size
    output = {
        'total': total,
        'data': [
            i.to_dict()
            for i
            in s[left_bound:right_bound]
            if total
        ]
    }
    return output
