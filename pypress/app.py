import BaseHTTPServer
from request import RequestHandler

router = {}

class Server(BaseHTTPServer.HTTPServer):
    def init(self, hostname, port, application):
        pass


class Application():
    def _app(environ, start_response):
        pass

    def __init__(self):
        self.app = _app

    def route(fn):
        def wrapper(*args, **kwargs):
            pass
        return wrapper

    
    def listen(port=1337, hostname='', backlog=511, callback=None):
        server = Server(hostname, port, self.app)
        server.serve_forever()

