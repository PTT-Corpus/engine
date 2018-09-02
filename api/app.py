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
        board = req.get_param('board', default='movie')
        output = query(word=word,
                       page=page,
                       size=size,
                       post_type=post_type,
                       board=board)
        resp.media = output


api = falcon.API()
api.add_static_route('/static', STATIC_PATH)
api.add_route('/query', Query())

SWAGGERUI_URL = '/swagger'
SCHEMA_URL = '/static/swagger.json'

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
