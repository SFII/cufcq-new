import tornado.web
from handlers.static_handler import StaticHandler
import os

class IndexHandler(StaticHandler):
    def get(self):
        pid = os.getpid()
        self.render('home.html', proccess=pid)
