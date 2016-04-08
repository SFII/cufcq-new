import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler

class NotFoundHandler(BaseHandler):
    def get(self):
        self.render('layouts/not_found.html')
