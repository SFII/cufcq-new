import tornado.web
import tornado.template


class InstructorHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('layouts/instructor_view.html')
