import BaseHTTPServer

router = {}

class Server(BaseHTTPServer.HTTPServer):
    pass

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass

class Application():
    def __init__(self):
        pass

    def route(fn):
        def wrapper(*args, **kwargs):
            pass
        return wrapper

    
    def listen(port=1337, hostname='', backlog=511, callback=None):
        server = Server(hostname, port, self.app)
        server.serve_forever()

