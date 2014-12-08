from .utils import methods

DEBUG_MODE = True


class Router():
    def __init__(self):
        self.routes = {}
        for method in methods:
            self._generate_add_route_method(method)

    # helper method for adding routes.
    # if middleware is provided, mount the middleware at the path.
    # if not, return a decorator that mounts the function as middleware at path.
    def _add_route(self, path, middleware=None, method='*'):
        if path not in self.routes:
            self.routes[path] = {}

        method = method.upper()
        if method not in self.routes[path]:
            self.routes[path][method] = []

        # the actual method that mounts the middleware to the route and method.
        # may be returned as a decorator.
        def add_route(f):
            self.routes[path][method].append(f)

        if DEBUG_MODE:
            print('mounting middleware %s at path %s' % (middleware, path))

        if middleware:
            for m in middleware:
                add_route(m)
        else:
            return add_route

    # generates an add_route method for EVERY HTTP method.
    # this is for app.get, app.post, app.trace, app.mkactivity, etc.
    def _generate_add_route_method(self, method):
        add_route = self._add_route
        if DEBUG_MODE:
            print('registering app.%s' % (method))

        def add_route_method(path='*', *middleware):
            if not isinstance(path, str):
                middleware = [path] + [m for m in middleware]
                path = '*'
            return add_route(path, middleware, method)

        # temporary solution ?? ? ? ?
        setattr(self, method, add_route_method)
        return getattr(self, method)

    # mount the middleware for all requests to the path.
    def use(self, path='*', *middleware):
        # path can be a piece of middleware
        # if so, append it to middleware
        if not isinstance(path, str):
            middleware = [path] + [m for m in middleware]
            path = '*'
        return self._add_route(path, middleware)

    def route(self, path='*'):
        pass
