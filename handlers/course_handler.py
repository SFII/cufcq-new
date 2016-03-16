import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler

class CourseHandler(tornado.web.RequestHandler):
    def get(self):
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
            course_info=course_info_object,
            instructor_stats=instructor_stats_object,
            department_info=department_info_object,
            instructor_fcqs=instructor_fcqs_array)
