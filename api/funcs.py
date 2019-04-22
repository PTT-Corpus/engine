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
          pos: bool=False,
          window_size: int=10) -> dict:
    """Query word."""
    s = Search(using=client, index='ptt')
    must = [
        Q('match', content=word)
    ]
    if post_type == 0 or post_type == 1:
        must.append(
            Q('match', post_type=post_type),
        )

    s.query = Q(
        'bool',
        must=must,
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

    # highlight
    s = s.highlight_options(number_of_fragments=0)
    s = s.highlight('content')
    total = s.count()
    left_bound = page * size
    right_bound = left_bound + size
    data = []
    if total:
        for i in s[left_bound:right_bound]:
            d = i.to_dict()
            if pos:
                segments = j.seg(d['content'], pos=True)
                for idx, (char, pos) in enumerate(segments):
                    segments[idx] = f'{char}|{pos}'
                    if char == word:
                        segments[idx] = f'<em>{segments[idx]}</em>'
                        left = idx - window_size
                        if left < 0:
                            left = 0
                        right = idx + window_size + 1
                        break
                d['concordance'] = (
                    ' '.join(segments[left:idx]),
                    segments[idx],
                    ' '.join(
                        f'{char}|{pos}'
                        for (char, pos)
                        in segments[idx+1:right]
                    ),
                )

            else:
                concordance = i.meta.highlight.content[0].replace('\n ', '')
                concordance = concordance.split(' ')
                for idx, word in enumerate(concordance):
                    if word.startswith('<em>'):
                        left = idx - window_size
                        if left < 0:
                            left = 0
                        right = idx + window_size + 1
                        d['concordance'] = (
                            ' '.join(concordance[left:idx]),
                            concordance[idx],
                            ' '.join(concordance[idx+1:right]),
                        )
                        break
            data.append(d)
    output = {
        'total': total,
        'page': page,
        'size': size,
        'data': data,
    }
    return output
