from .app import Application
from .router import Router
from .middleware import Middleware

Pypress = Application
Pypress.Router = Router
Pypress.Middleware = Middleware
