"""
Routing configuration.
"""
from handlers.index_handler import IndexHandler
from handlers.instructor_handler import InstructorHandler
# from handlers.course_handler import CourseHandler
# from handlers.department_handler import DepartmentHandler
from handlers.api_handler import ApiHandler
# Tornado pro-tip: regex routing is optimized by putting more frequently
# accessed routes and simpler regexes before other routes.
routes = [
    (r"/", IndexHandler),
    (r"/instructors", InstructorHandler),
    # (r"/courses", CourseHandler),
    # (r"/departments", DepartmentHandler),
    # (r"/instructor/([\w-]+)", InstructorHandler),
    (r"/api/(instructor|course|fcq|department)/([\w-]+)", ApiHandler)
]
