from wsgiref.simple_server import make_server

router = {}

class Application():
	def __init__(self):
		print 5

def route(fn):
	def wrapper(*args, **kwargs):
		pass
	return wrapper

def listen(port=1337, hostname=''):
	server_class = BaseHTTPServer.BaseHTTPServer
	request_handler_class = BaseHTTPServer.BaseHTTPRequestHandler
	server = server_class((hostname, port), request_handler_class)
	server.serve_forever()