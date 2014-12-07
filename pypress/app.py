import http.server
from .request import Request
from .response import Response
from .router import Router
from .methods import methods


class PypressServer(http.server.HTTPServer):
    pass


class PypressRequestHandler(http.server.BaseHTTPRequestHandler):
    routes = {}

    def construct_middleware_stack(self, route, method):
        pass

    def handle_request(self):
        req = Request(self)
        res = Response(self)
        middleware_stack = construct_middleware_stack(self.path, self.command)


class Application():
    Router = Router
    routes = {}

    def __init__(self):
        # generates a route adder for every HTTP method.
        for method in methods:
            self._generate_add_route_method(method)

    # helper method for adding routes.
    # if middleware is provided, mount the middleware at the path.
    # if not, return a decorator that mounts the function as middleware at path.
    def _add_route(self, path, middleware=None, method=None):
        if path not in self.routes:
            self.routes[path] = {} if method else []

        if method and (method not in self.routes[path]):
            self.routes[path][method] = []

        def add_route(f):
            route_middleware = self.routes[path][method] if method \
                else self.routes[path]
            route_middleware.append(f)

        if middleware:
            for m in middleware:
                add_route(m)
        else:
            return add_route

    # generates an add_route method for EVERY method.
    # this is for app.get, app.post, app.trace, app.mkactivity, etc.
    def _generate_add_route_method(self, method):
        add_route = self._add_route
        def add_route_method(self, path='*', *middleware):
            return add_route(path, middleware, method)

        # temporary solution ?? ? ? ?
        setattr(self, method, add_route_method)
        return add_route_method

    # mount the middleware for all requests to the path.
    def use(self, path='*', *middleware):
        return self._add_route(path, middleware)

    def route(self, path='*'):
        pass

    def listen(self, port=1337, hostname='', backlog=511, callback=None):
        server_address = ('', 1337)
        PypressRequestHandler.routes = self.routes
        for method in methods:
            setattr(PypressRequestHandler,
                    'do_{0}'.format(method.upper()),
                    PypressRequestHandler.handle_request)
        server = PypressServer(server_address, PypressRequestHandler)
        server.serve_forever()
