import tornado.web
from handlers.base_handler import BaseHandler

class AboutHandler(BaseHandler):
    def get(self):
        self.render('layouts/about.html')
        return
