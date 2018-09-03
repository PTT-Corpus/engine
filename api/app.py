"""PTT Engine API."""
import falcon
from falcon_swagger_ui import register_swaggerui_app

from funcs import query
from settings import (
    STATIC_PATH,
)


class Query:
    """Test."""

    def on_get(self, req, resp):
        """GET method."""
        word = req.get_param('word', required=True)
        page = req.get_param_as_int('page') or 0
        size = req.get_param_as_int('size') or 10
        post_type = req.get_param_as_int('post_type')
        boards = req.get_param_as_list('boards') or ['movie']
        sort = req.get_param('sort', default='published')
        order = req.get_param('order', default='desc')
        start = req.get_param_as_date('start') or None
        end = req.get_param_as_date('end') or None
        output = query(word=word,
                       page=page,
                       size=size,
                       post_type=post_type,
                       boards=boards,
                       sort=sort,
                       order=order,
                       start=start,
                       end=end)
        resp.media = output


api = falcon.API()
api.add_static_route('/static', STATIC_PATH)
api.add_route('/query', Query())

SWAGGERUI_URL = '/api'
SCHEMA_URL = 'http://140.112.147.121:9000/static/spec.json'

page_title = 'PTT Engine API'
favicon_url = (
    'http://lopen.linguistics.ntu.edu.tw/static_pttcorp/images/PTTCorp.ico')

register_swaggerui_app(
    api,
    SWAGGERUI_URL,
    SCHEMA_URL,
    page_title=page_title,
    favicon_url=favicon_url,
    config={'supportedSubmitMethods': ['get']}
)
