
def _header_to_dict(header_message):
    header_message = header_message.as_string()
    headers = [tuple(h.split(': ', 1)) for h in header_message.split('\n') if h]
    return {key: val for key, val in headers}


class Request():
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.headers = _header_to_dict(self.request_handler.headers)
        self.params = self.request_handler.params
        self.query = self.request_handler.query
        if 'Content-Length' in self.request_handler.headers:
            content_length = int(self.request_handler.headers['Content-Length'])
            self.body = self.request_handler.rfile.read(content_length).decode()
