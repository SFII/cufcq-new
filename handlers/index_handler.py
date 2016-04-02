import tornado.web
from handlers.static_handler import StaticHandler


class IndexHandler(StaticHandler):
    def get(self):
        self.render('home.html')
