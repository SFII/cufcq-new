import tornado.web
import logging
import json
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