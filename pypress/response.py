import json
import mimetypes


class Response():
    def __init__(self, request_handler):
        self.request_handler = request_handler
        mimetypes.init()

    # sets HTTP header as per given field and value.
    def set(self, field, value):
        self.request_handler.send_header(field, value)

    # header is an alias for set.
    header = set

    # sets the mimetype of the response body.
    def type(self, body_type):
        if ('/'in body_type):
            mimetype = body_type
        else:
            # check if body_type looks like a proper filename
            # if not, add 'a.' before it
            # SUPER HACKY!!!!!!
            body_type = body_type if ('.' in body_type) else ('a.' + body_type)
            mimetype = mimetypes.guess_type(body_type)[0]
        self.set('Content-Type', mimetype)

    # sets the response status
    def status(self, code):
        self.res_status = code
        return self

    # sends response, status optional as 1st argument, followed by body
    def send(self, *args):
        # support for optional status code as 1st arg
        if isinstance(args[0], int):
            self.res_status = args[0]
            self.body = args[1] if (len(args) > 1) else ''
        else:
            self.body = args[0]
            if not hasattr(self, 'res_status'):
                # temp, should be changeable
                self.res_status = 200 if self.body else 500

        self.request_handler.send_response(self.res_status)
        self.request_handler.end_headers()

        self.request_handler.wfile.flush()
        self.request_handler.wfile.write(bytes(str(self.body), 'UTF-8'))
        self.request_handler.wfile.flush()

    def json(self, data):
        self.type('json')
        self.send(json.dumps(data))
