import json

# a library of standard middleware.


class Middleware():
    def json_body_parser(req, res, next):
        # parse json here
        if hasattr(req, 'body'):
            req.body = json.loads(req.body)
        next()
