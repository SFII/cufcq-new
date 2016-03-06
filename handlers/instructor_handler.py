import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler

class InstructorHandler(BaseHandler):
    
    def get(self,id):
        
        instructor = self.application.settings['instructor'].get_item(id)
        if instructor is None: 
            #404 goes here
            return

        print(instructor)
        instructor_info_object = {
            "first_name" : instructor.get('instructor_first').title(),
            "last_name" : instructor.get('instructor_last').title(),
            "department" : instructor.get('department_id').upper(),
            # TODO
            "type" : "TTT",
            "sections" : len(instructor.get('fcqs')),
            "courses" : len(instructor.get('courses')),
            "last_fcq" : self.convert_date(instructor.get('fcqs_yearterms')[-1]),
            "first_fcq" : self.convert_date(instructor.get('fcqs_yearterms')[0]),
        }
        instructor_stats_object = {
            "effectiveness" : 5,
            "overall" : 3,
            "availability" : 6,
            "respect" : 2,
        }

        department_info_object = {
            "name" : "Computer Science",
            "num_ugrads" : 556,
            "num_grads" : 43,
            "num_courses" : 5,
            "average_workload" : "4hrs",
            # NOT TAs,
            "num_instructors" : 58,
            "first_fcq" : "Spring 2012",
        }
        class1 = {
            "name" : "Spring 2015 ACCT 5220-2 Playing with Dildos",
            "info" : "All you need to know!",
            "sdfjksjkdf" : 'akjhsdakljsdjklasd',
        }
        class2 = {
            "name" : "Fall 2014 PSYCH 1300-2 Amateur Freud",
            "info" : "Facts out the wazoo!",
            "sdfjksjkdf" : 'akjhsdakljsdjklasd',
        }
        class3 = {
            "name" : "Fall 2013 CSCI 5001-2 Making Moneyzz",
            "info" : "Daddy Warbucks!",
            "sdfjksjkdf" : 'akjhsdakljsdjklasd',
        }
        instructor_fcqs_array = [
        class1,class2,class3
        ]
        self.render('layouts/instructor_view.html',
            instructor_info=instructor_info_object,
            instructor_stats=instructor_stats_object,
            department_info=department_info_object,
            instructor_fcqs=instructor_fcqs_array)
