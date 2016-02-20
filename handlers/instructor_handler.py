import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler


class InstructorHandler(BaseHandler):

    # index
    def get(self, input):
        self.render('layouts/instructor_view.html')

    # read
    def get(self):
        self.render('layouts/instructor_view.html')
