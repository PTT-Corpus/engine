"""PTT Engine API."""
import falcon


class Test:
    """Test."""

    def on_get(self, req, resp):
        """GET method."""
        output = {
            'name': 'Aji',
            'message': 'this is a test'
        }
        resp.media = output


api = falcon.API()
api.add_route('/', Test())
