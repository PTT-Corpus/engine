"""PTT Engine API."""
import falcon
from falcon_swagger_ui import register_swaggerui_app

from funcs import query
from settings import (
    STATIC_PATH,
    SWAGGERUI_URL,
    SCHEMA_URL,
    PAGE_TITLE,
    FAVICON_URL,
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


register_swaggerui_app(
    api,
    SWAGGERUI_URL,
    SCHEMA_URL,
    page_title=PAGE_TITLE,
    favicon_url=FAVICON_URL,
    config={'supportedSubmitMethods': ['get']}
)
