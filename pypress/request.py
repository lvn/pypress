

class Request():
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.params = self.request_handler.params
        self.query = self.request_handler.query
        if 'Content-Length' in self.request_handler.headers:
            content_length = int(self.request_handler.headers['Content-Length'])
            self.body = self.request_handler.rfile.read(content_length).decode()
