import json
import mimetypes


class Response():
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.headers = {}
        mimetypes.init()

    def set(self, field, value):
        """Sets the HTTP header of the given field to the given value."""
        self.headers[field] = value

    # header is an alias for set.
    header = set

    def type(self, body_type):
        """Sets/gueses the mimetype of the response body."""
        if ('/'in body_type):
            mimetype = body_type
        else:
            # check if body_type looks like a proper filename
            # if not, add 'a.' before it
            # SUPER HACKY!!!!!!
            body_type = body_type if ('.' in body_type) else ('a.' + body_type)
            mimetype = mimetypes.guess_type(body_type)[0]
        self.set('Content-Type', mimetype)

    def status(self, code):
        """Sets the response status."""
        self.res_status = code
        return self

    def send(self, *args):
        """Send response status and body. Status optional as 1st argument."""
        # support for optional status code as 1st arg
        if isinstance(args[0], int):
            self.res_status = args[0]
            self.body = args[1] if (len(args) > 1) else ''
        else:
            self.body = args[0]
            if not hasattr(self, 'res_status'):
                # temp, should be changeable
                self.res_status = 200 if self.body else 500

        self.request_handler.wfile.write(bytes(str(self.body), 'UTF-8'))
        self.request_handler.wfile.flush()

        self.request_handler.send_response(self.res_status)
        for field, value in self.headers.items():
            self.request_handler.send_header(field, value)
        self.request_handler.end_headers()

    def json(self, data):
        """Sets the mimetype header to JSON before sending the response."""
        self.type('json')
        self.send(json.dumps(data))
