"""
Routing configuration.
"""
from handlers.indexhandler import IndexHandler
# Tornado pro-tip: regex routing is optimized by putting more frequently
# accessed routes and simpler regexes before other routes.
routes = [
    (r"/", IndexHandler),
]
