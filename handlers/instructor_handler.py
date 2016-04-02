import tornado.web
import tornado.template
import logging
from handlers.base_handler import BaseHandler

class InstructorHandler(BaseHandler):

    def color(self, course_data):
        return 'primary'

    def keywords_string(self, instructor_data):
        first_name = instructor_data.get('instructor_first').title()
        last_name = instructor_data.get('instructor_last').title()
        return """{0},{1},cufcq,university,colorado,faculty,course,instructor,
        fcq,grade,department,database""".format(first_name, last_name)

    def description_string(self, instructor_data):
        first_name = instructor_data.get('instructor_first').title()
        last_name = instructor_data.get('instructor_last').title()
        instructor_description = {
            'TTT': "Tenured or Tenured-Track Instructor",
            'OTH': "Instructor",
            'TA': "Teaching Assistant"
        }[instructor_data['instructor_group']]
        campus_location = self.convert_campus(instructor_data['campus'])
        return """{0} {1} is a {2} at the University of Colorado, {3}. CUFCQ is
        a data analysis project for studying and visualizing the University of
        Colorado's Faculty Course Questionnaire data.""".format(first_name, last_name, instructor_description, campus_location)

    def overtime_linechart_data(self, raw_data):

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
        yearterms = raw_data['fcqs_yearterms']
        overtime_data = raw_data['fcqs_overtime']
        labels = list(map(self.convert_date, yearterms))
        datasets = list(map(_overtime_dataset_builder, keys))
        return tornado.escape.json_encode({
            'labels': labels,
            'datasets': datasets,
        })

    def get(self, id):
        instructor = self.application.settings['instructor'].get_item(id)
        if instructor is None:
            self.redirect('/notFound')
            return

        instructor_info_object = {
            "first_name": instructor.get('instructor_first').title(),
            "last_name": instructor.get('instructor_last').title(),
            "department": instructor.get('department_id').upper(),
            "type": instructor.get('instructor_group'),
            "sections": len(instructor.get('fcqs')),
            "courses": len(instructor.get('courses')),
            "last_fcq": self.convert_date(instructor.get('fcqs_yearterms')[-1]),
            "first_fcq": self.convert_date(instructor.get('fcqs_yearterms')[0]),
        }
        instructor_stats_object = {
            "effectiveness": round(instructor.get('fcqs_stats').get('instructor_effectiveness_average'), 1),
            "overall": round(instructor.get('fcqs_stats').get('instructoroverall_average'), 1),
            "availability": round(instructor.get('fcqs_stats').get('instructor_availability_average'), 1),
            "respect": round(instructor.get('fcqs_stats').get('instructor_respect_average'), 1),
        }

        # fcqs = self.get_fcq_data(instructor.get('fcqs'))
        fcqs = instructor.get('fcqs', [])

        chart_data = self.overtime_linechart_data(instructor)

        self.render('layouts/instructor_view.html',
                    raw_data=instructor,
                    instructor_info=instructor_info_object,
                    instructor_stats=instructor_stats_object,
                    instructor_fcqs=fcqs)
