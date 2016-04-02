"""
Routing configuration.
"""
from handlers.index_handler import IndexHandler
from handlers.instructor_handler import InstructorHandler
from handlers.course_handler import CourseHandler
from handlers.department_handler import DepartmentHandler
from handlers.api.api_handler import ApiHandler
from handlers.ajax.fcqcard_handler import FcqCardHandler
from handlers.foobar import Foobar
from handlers.not_found_handler import NotFoundHandler
from handlers.about_handler import AboutHandler
# Tornado pro-tip: regex routing is optimized by putting more frequently
# accessed routes and simpler regexes before other routes.
routes = [
    (r"/", IndexHandler),
    (r"/foobar", Foobar),
    (r"/ajax/fcqcard/([\w-]+)", FcqCardHandler),
    (r"/instructor/([\w-]+)", InstructorHandler),
    (r"/course/([\w-]+)", CourseHandler),
    (r"/department/([\w-]+)", DepartmentHandler),
    (r"/api/(instructor|course|fcq|grade|department)/([\w-]+)", ApiHandler),
    (r"/notFound", NotFoundHandler)
#    (r"/about", AboutHandler)
]
