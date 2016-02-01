import tornado.web
from handlers.statichandler import StaticHandler


class IndexHandler(StaticHandler):
    def get(self):
        self.render('static/home.html')
