import BaseHTTPServer
from .request import Request
from .response import Response
from .router import Router


class PypressServer(BaseHTTPServer.HTTPServer):
    pass


class PypressRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def handle_request(self):
        pass

    do_GET = handle_request
    do_POST = handle_request
    do_PUT = handle_request
    do_PATCH = handle_request
    do_DELETE = handle_request


class Application():
    Router = Router

    def __init__(self):
        self.routes = {}

    # helper method to mount middleware for the given route and method.
    # if no method is provided, mount the middleware for all methods.
    def _mount_middleware(self, path, middleware, method=None):
        middleware = [m for m in middleware]
        if not self.routes[path]:
            self.routes[path] = {} if method else []
        if method:
            # mount middleware for method
            if not self.routes[path][method]:
                self.routes[path][method] = []
            self.routes[path][method] += middleware
        else:
            self.routes.path += middleware

    # mount the middleware for all requests to the path.
    def use(self, path, *middleware):
        if middleware:
            self._mount_middleware(path, middleware)
        else:
            def add_route(f):
                self.routes[path] = f
            return add_route

    # mount the middleware for all GET requests to the path.
    def get(self, path, *middleware):
        if middleware:
            self._mount_middleware(path, middleware, 'GET')
        else:
            def add_route(f):
                self.routes[path] = f
            return add_route

    # mount the middleware for all POST requests to the path.
    def post(self, path, *middleware):
        if middleware:
            self.routes[path] = middleware
        else:
            def add_route(f):
                self.routes[path] = f
            return add_route

    # mount the middleware for all PUT requests to the path.
    def put(self, path, *middleware):
        if middleware:
            self.routes[path] = middleware
        else:
            def add_route(f):
                self.routes[path] = f
            return add_route

    # mount the middleware for all GET requests to the path.
    def patch(self, path, *middleware):
        if middleware:
            self.routes[path] = middleware
        else:
            def add_route(f):
                self.routes[path] = f
            return add_route

    # mount the middleware for all DELETE requests to the path.
    def delete(self, path, *middleware):
        if middleware:
            self.routes[path] = middleware
        else:
            def add_route(f):
                self.routes[path] = f
            return add_route

    def listen(port=1337, hostname='0.0.0.0', backlog=511, callback=None):
        server = PypressServer((hostname, port), PypressRequestHandler)
        server.serve_forever()
