"""PTT Engine API."""
import falcon

from funcs import query


class Query:
    """Test."""

    def on_get(self, req, resp):
        """GET method."""
        word = req.get_param('word', required=True)
        page = req.get_param_as_int('page') or 0
        size = req.get_param_as_int('size') or 10
        post_type = req.get_param_as_int('post_type')
        board = req.get_param('board', default='movie')
        sort = req.get_param('sort', default='published')
        order = req.get_param('order', default='desc')
        output = query(word=word,
                       page=page,
                       size=size,
                       post_type=post_type,
                       board=board,
                       sort=sort,
                       order=order)
        resp.media = output


api = falcon.API()
api.add_route('/query', Query())
