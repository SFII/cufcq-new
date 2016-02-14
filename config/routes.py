"""
Routing configuration.
"""
from handlers.index_handler import IndexHandler
from handlers.instructor_handler import InstructorHandler
# Tornado pro-tip: regex routing is optimized by putting more frequently
# accessed routes and simpler regexes before other routes.
routes = [
    (r"/", IndexHandler),
    (r"/instructor", InstructorHandler)
]
