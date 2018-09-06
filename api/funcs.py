"""Core functions."""
from datetime import datetime

from elasticsearch_dsl import (
    Search,
    Q,
)
from jseg import Jieba

from settings import get_client


client = get_client()
j = Jieba()


def query(word: str,
          page: int,
          size: int,
          post_type: int,
          boards: list,
          sort: str,
          order: str,
          start: datetime=None,
          end: datetime=None,
          pos: bool=False) -> dict:
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
    data = []
    if total:
        for i in s[left_bound:right_bound]:
            d = i.to_dict()
            if pos:
                res = [
                    f'{word}|{pos}'
                    for (word, pos)
                    in j.seg(d['content'], pos=True)
                ]
                d['content'] = ' '.join(res)
            data.append(d)
    output = {
        'total': total,
        'data': data,
    }
    return output
