import tornado.web
import logging
import json
import rethinkdb as r
from functools import wraps


class BaseHandler(tornado.web.RequestHandler):

    def render(self, template_name, **kwargs):
        raw_data = kwargs.get('raw_data', '')
        kwargs['keywords_string'] = self.keywords_string(raw_data)
        kwargs['description_string'] = self.description_string(raw_data)
        kwargs['linechart_data'] = self.overtime_linechart_data(raw_data)
        kwargs['color'] = self.color()
        kwargs['convert_date'] = self.convert_date
        kwargs['convert_campus'] = self.convert_campus
        kwargs['noneCheck'] = self.noneCheck
        super().render(template_name, **kwargs)

    def color(self):
        return 'primary'

    def keywords_string(self, raw_data):
        return """cufcq,university,colorado,faculty,course,instructor,fcq,grade,department,database"""

    def noneCheck(self, raw_data):
        if(raw_data is not None):
            round(raw_data, 1)
        else:
            return 0
        
    def description_string(self, raw_data):
        return """CUFCQ is a data analysis project for studying and visualizing
        the University of Colorado's Faculty Course Questionnaire data."""

    def convert_date(self, yearterm):
        if(yearterm == ''):
            return ''
        VALID_TERMS = {'1': 'Spring', '4': 'Summer', '7': 'Fall'}
        yearterm_str = str(yearterm)
        year = yearterm_str[0:4]
        term = VALID_TERMS.get(yearterm_str[4])
        return '{0} {1}'.format(term, year)

    def convert_campus(self, campus):
        return {
            'BD': 'CU Boulder',
            'DN': 'CU Denver',
            'CS': 'CU Colorado Springs',
        }[campus]

    def convert_level(self, level):
        return {
            'GR': "Graduate Level",
            'UD': "Upper Division",
            'LD': "Lower Division"
        }[level]

    def fcq_title(self, fcq_data):
        date = self.convert_date(fcq_data['yearterm'])
        campus = self.convert_campus(fcq_data['campus'])
        course_title = fcq_data['course_title']
        course_subject = fcq_data['course_subject']
        course_number = fcq_data['course_number']
        course_name = "{0}-{1} {2}".format(course_subject, course_number, course_title)
        return "{0} {1} {2}".format(campus, date, course_name)

    def get_fcq_data(self, fcq_ids):
        db = self.application.settings['database_name']
        conn = self.application.settings['conn']
        fcq_data = list(r.db(db).table('Fcq').get_all(r.args(fcq_ids)).run(conn))
        return list(map(lambda fcq:
                    dict(fcq_title=self.fcq_title(fcq), **fcq),
                    fcq_data))

    def overtime_linechart_data(self, raw_data):
        return tornado.escape.json_encode({
            'labels': [],
            'datasets': [],
        })
