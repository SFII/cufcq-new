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
        if course is None:
            # 404 goes here
            return
        course_info_object = {
            "code": "ACCT 3220",
            "title": "Corp Financial Rprtng 1",
            "department": "Accounting",
            "sections": 79,
            "students": 2578,
            "last_fcq": "Spring 2015",
            "first_fcq": "Spring 2012",
        }
        instructor_stats_object = {
            "effectiveness": 5,
            "overall": 3,
            "availability": 6,
            "respect": 2,
        }

        department_info_object = {
            "name": "Computer Science",
            "num_ugrads": 556,
            "num_grads": 43,
            "num_courses": 5,
            "average_workload": "4hrs",
            # NOT TAs,
            "num_instructors": 58,
            "first_fcq": "Spring 2012",
        }
        class1 = {
            "name": "Spring 2015 ACCT 5220-2 Playing with Dildos",
            "info": "All you need to know!",
            "sdfjksjkdf": 'akjhsdakljsdjklasd',
        }
        class2 = {
            "name": "Fall 2014 PSYCH 1300-2 Amateur Freud",
            "info": "Facts out the wazoo!",
            "sdfjksjkdf": 'akjhsdakljsdjklasd',
        }
        class3 = {
            "name": "Fall 2013 CSCI 5001-2 Making Moneyzz",
            "info": "Daddy Warbucks!",
            "sdfjksjkdf": 'akjhsdakljsdjklasd',
        }
        instructor_fcqs_array = [
        class1,class2,class3
        ]
        self.render('layouts/course_view.html',
            raw_data=course,
            course_info=course_info_object,
            instructor_stats=instructor_stats_object,
            department_info=department_info_object,
            instructor_fcqs=instructor_fcqs_array)
