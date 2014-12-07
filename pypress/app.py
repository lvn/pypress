import http.server
from .request import Request
from .response import Response
from .router import Router


class PypressServer(http.server.HTTPServer):
    pass


class PypressRequestHandler(http.server.BaseHTTPRequestHandler):
    routes = {}

    def handle_request(self):
        print(self.routes)
        pass

    do_GET = handle_request
    do_POST = handle_request
    do_PUT = handle_request
    do_PATCH = handle_request
    do_DELETE = handle_request


class Application():
    Router = Router
    routes = {}

    def __init__(self):
        pass

    # helper method for adding routes.
    # if middleware is provided, mount the middleware at the path.
    # if not, return a decorator that mounts the function as middleware at path.
    def _add_route(self, path, middleware=None, method=None):

        if path not in self.routes:
            self.routes[path] = {} if method else []

        if method and (method not in self.routes[path]):
            self.routes[path][method] = []

        def add_route(f):
            route_dict = self.routes[path][method] if method \
                else self.routes[path]
            route_dict.append(f)

        if middleware:
            for m in middleware:
                add_route(m)
        else:
            return add_route

    # mount the middleware for all requests to the path.
    def use(self, path='*', *middleware):
        return self._add_route(path, middleware)

    # mount the middleware for all GET requests to the path.
    def get(self, path='*', *middleware):
        return self._add_route(path, middleware, 'GET')

    # mount the middleware for all POST requests to the path.
    def post(self, path='*', *middleware):
        return self._add_route(path, middleware, 'POST')

    # mount the middleware for all PUT requests to the path.
    def put(self, path='*', *middleware):
        return self._add_route(path, middleware, 'PUT')

    # mount the middleware for all GET requests to the path.
    def patch(self, path='*', *middleware):
        return self._add_route(path, middleware, 'PATCH')

    # mount the middleware for all DELETE requests to the path.
    def delete(self, path='*', *middleware):
        return self._add_route(path, middleware, 'DELETE')

    def route(self, path='*'):
        pass

    def listen(self, port=1337, hostname='', backlog=511, callback=None):
        server_address = ('', 1337)
        PypressRequestHandler.routes = self.routes
        server = PypressServer(server_address, PypressRequestHandler)
        server.serve_forever()
