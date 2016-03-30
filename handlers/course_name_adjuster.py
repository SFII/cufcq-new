import tornado.web
import logging
import json
import rethinkdb as r
from functools import wraps


class CourseNameAdjuster(tornado.web.RequestHandler):
    cursor = self.application.settings['course'].cursor()

    def get(self):
        try:
            course_data = cursor.next()
        except ReqlCursorEmpty:
            self.write("all done!")
        

    def post(self):
        self.process_post(data)
        self.get()

    def process_post(self, data):
