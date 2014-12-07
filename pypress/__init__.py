from .app import Application
from .router import Router

Pypress = Application
setattr(Pypress, 'Router', Router)
