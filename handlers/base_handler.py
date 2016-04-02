import tornado.web
import logging
import json
import rethinkdb as r
from functools import wraps


class BaseHandler(tornado.web.RequestHandler):

    def render(self, template_name, **kwargs):
        raw_data = kwargs.get('raw_data','')
        kwargs['keywords_string'] = self.keywords_string(raw_data)
        kwargs['description_string'] = self.description_string(raw_data)
        super().render(template_name, **kwargs)

    def keywords_string(self, raw_data):
        return """cufcq,university,colorado,faculty,course,instructor,fcq,grade,department,database"""

    def description_string(self, raw_data):
        return """CUFCQ is a data analysis project for studying and visualizing
        the University of Colorado's Faculty Course Questionnaire data."""

    def convert_date(self, yearterm):
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

    def overtime_linechart_data(self, model_data):

        def _overtime_builder(overtime_data, key):
            def _transform_overtime_data(yearterm):
                return round(overtime_data[str(yearterm)][key], 1)
            return _transform_overtime_data

        def _overtime_dataset_builder(key):
            color = {
                'instructor_effectiveness_average': (247, 92, 3),
                'instructor_respect_average': (217, 3, 104),
                'instructoroverall_average': (130, 2, 99),
                'instructor_availability_average': (4, 167, 119)
            }[key]
            label = {
                'instructor_effectiveness_average': 'Effectiveness',
                'instructor_respect_average': 'Respect',
                'instructoroverall_average': 'Overall',
                'instructor_availability_average': 'Availability'
            }[key]
            return {
                'label': label,
                'fillColor': "rgba({0},{1},{2},0.2)".format(*color),
                'strokeColor': "rgba({0},{1},{2},1)".format(*color),
                'pointColor': "rgba({0},{1},{2},1)".format(*color),
                'pointHighlightStroke': "rgba({0},{1},{2},1)".format(*color),
                'pointStrokeColor': "#fff",
                'pointHighlightFill': "#fff",
                'data': list(map(_overtime_builder(overtime_data, key), yearterms))
            }

        keys = [
            'instructor_effectiveness_average',
            'instructor_respect_average',
            'instructoroverall_average',
            'instructor_availability_average'
        ]
        yearterms = model_data['fcqs_yearterms']
        overtime_data = model_data['fcqs_overtime']
        labels = list(map(self.convert_date, yearterms))
        datasets = list(map(_overtime_dataset_builder, keys))
        return tornado.escape.json_encode({
            'labels': labels,
            'datasets': datasets,
        })
