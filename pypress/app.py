import re
import urllib
import http.server
from .request import Request
from .response import Response
from .router import Router
from .utils import methods

DEBUG_MODE = False


class PypressServer(http.server.HTTPServer):
    pass


class PypressRequestHandler(http.server.BaseHTTPRequestHandler):
    routes = {}

    # perform route match between rule and request.
    # for now, just match route segments.
    # return a dictionary of route params, or False if no match.
    def route_match(self, route_rule, route_req):
        if DEBUG_MODE:
            print('trying to match routes: ', route_rule, route_req)
        rule_parts = [part for part in route_rule.split('/') if part]
        req_parts = [part for part in route_req.split('/') if part]
        params = {}

        # TODO: refactor, needs better sync loop
        for rule_part in rule_parts:
            if req_parts:
                req_part = req_parts.pop(0)
                if DEBUG_MODE:
                    print('matching parts: ', rule_part, req_part)
            else:
                return False

            if rule_part == '*':
                continue
            elif rule_part[0] == ':':
                params[rule_part[1:]] = req_part
            else:
                if rule_part != req_part:
                    return False
        else:
            if req_parts:
                return False
        return params

    # routes
    def get_middleware(self, path, method):
        middleware = []
        self.params = {}

        # TODO: refactor to better account for *
        # TODO: handle routers

        if '*' in self.routes:
            if isinstance(self.routes['*'], dict):
                if '*' in self.routes['*']:
                    middleware = self.routes['*']['*'] + middleware
                if method in self.routes['*']:
                    middleware = self.routes['*'][method] + middleware
            elif isinstance(self.routes['*'], Router):
                # handle as Router object
                pass

        for rule in self.routes:
            route_match = self.route_match(rule, path)
            if rule != '*' and route_match is not False:
                self.params = route_match
                if isinstance(self.routes[rule], dict):
                    if '*' in self.routes[rule]:
                        middleware += self.routes[rule]['*']
                    if method in self.routes[rule]:
                        middleware += self.routes[rule][method]
                elif isinstance(self.routes[rule], Router):
                    # handle as Router object
                    pass
                break
        else:
            # no route match
            return False

        if DEBUG_MODE:
            print(middleware)
        return middleware

    def next(self):
        next_middleware = self.middleware.pop(0)
        return (next_middleware(self.req, self.res, self.next)
                if (next_middleware.__code__.co_argcount == 3)
                else next_middleware(self.req, self.res))

    call_middleware = next

    # the basic request handling method.
    # responsible for assembling middleware, and then invoking them
    def handle_request(self):
        if '?' in self.path:
            self.path, self.query = tuple(self.path.split('?'))
            self.query = {param[0]: urllib.parse.unquote_plus(param[1])
                          for param in [tuple(query_pair.split('='))
                          for query_pair in self.query.split('&')]}
        else:
            self.query = {}

        self.middleware = self.get_middleware(self.path, self.command)
        self.req = Request(self)
        self.res = Response(self)
        if self.middleware:
            self.call_middleware()
        else:
            # handle error
            print ('no route match for %s %s' % (self.command, self.path))
            self.res.send(400)
            pass


class Application():
    routes = {}

    def __init__(self):
        # generates a route adder for every HTTP method.
        self.router = Router()

    def __getattr__(self, name):
        return getattr(self.router, name)

    def listen(self, port=1337, hostname='', backlog=511, callback=None):
        server_address = (hostname, port)
        PypressRequestHandler.routes = self.router.routes
        # sets all the do_* in PypressRequestHandler to handle_request
        # hacky?
        for method in methods:
            setattr(PypressRequestHandler,
                    'do_{0}'.format(method.upper()),
                    PypressRequestHandler.handle_request)
        server = PypressServer(server_address, PypressRequestHandler)
        if DEBUG_MODE:
            print('routes: ', self.router.routes)
            print('app listening on %s:%s' % server_address)
            print('IT\'S ALIVE')
        server.serve_forever()
