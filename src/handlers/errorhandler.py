import tornado.web
import logging
from models.user import User
from handlers.base_handler import BaseHandler

class PageNotFoundHandler(BaseHandler):
    def get(self):
        self.render("error.html")

    def post(self):
        self.render("error.html")

    def initialize(self, status_code):
        self.set_status(status_code)
