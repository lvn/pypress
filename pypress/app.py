from wsgiref.simple_server import make_server

router = {}

class Application():
    def _app(environ, start_response):
        pass

    def __init__(self):
        self.app = _app

    def route(fn):
        def wrapper(*args, **kwargs):
            pass
    return wrapper

    
    def listen(port=1337, hostname=''):
        server = make_server(hostname, port, self.app)
        server.serve_forever()

