

class Response():
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def set(self, field, value):
        self.request_handler.send_header(field, value)

    header = set

    def send(self):
        pass
