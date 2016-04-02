import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler

class CourseHandler(BaseHandler):

    def keywords_string(self, course_data):
        course_subject = course_data['course_subject']
        course_number = course_data['course_number']
        alternate_titles = course_data['alternate_titles']
        return """{0},{1},{2},cufcq,university,colorado,faculty,course,course,
        fcq,grade,department,database""".format(course_subject, course_number, ','.join(alternate_titles))

    def description_string(self, course_data):
        course_subject = course_data['course_subject']
        course_number = course_data['course_number']
        course_title = course_data['course_title']
        course_level = self.convert_level(course_data['level'])
        campus_location = self.convert_campus(course_data['campus'])
        return """{0} {1}: {2} is a {3} course at the University of Colorado, {4}. CUFCQ is
        a data analysis project for studying and visualizing the University of
        Colorado's Faculty Course Questionnaire data.""".format(course_subject, course_number, course_title, course_level, campus_location)

    def get(self, id):
        course = self.application.settings['course'].get_item(id)
        print(course)
        if course is None:
            self.redirect('/notFound')
            return
        
        course_info_object = {
            "title": course.get('course_title'),
            "id": course.get('id'),
            "campus": self.convert_campus(course.get('campus')),
            "department": course.get('department_id'),
            "subject": course.get('course_subject'),
            "sections": len(course.get('fcqs')),
            "instructors": course.get('fcqs_stats').get('total_instructors'),
        }

        course_stats_object = {
            "challenge": round(course.get('fcqs_stats').get('course_challenge_average'), 1),
            "learned": round(course.get('fcqs_stats').get('course_howmuchlearned_average'), 1),
            "overall": round(course.get('fcqs_stats').get('courseoverall_average'), 1),
            "workload": course.get('hours_per_week_in_class_string')        
        }

        fcqs = course.get('fcqs', [])

        self.render('layouts/course_view.html',
            raw_data=course,
            course_info=course_info_object,
            course_stats=course_stats_object,
            course_fcqs=fcqs,
            color='orange')
