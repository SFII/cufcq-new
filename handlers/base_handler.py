import tornado.web
import logging
import json
import rethinkdb as r
from functools import wraps


class BaseHandler(tornado.web.RequestHandler):

    def convert_date(self, date):
        VALID_TERMS = {'1': 'Spring', '4': 'Summer', '7': 'Fall'}

        date_str = str(date)
        year = date_str[0:4]
        term = VALID_TERMS.get(date_str[4])

        return '{0} {1}'.format(term,year)

    def convert_campus(self, campus):
        CAMPUS_CODES = ['BD', 'DN', 'CS']

    def get_fcq_data(self, fcq_ids):
        db = self.application.settings['database_name']
        conn = self.application.settings['conn']
        return list(r.db(db).table('Fcq').get_all(r.args(fcq_ids)).run(conn))