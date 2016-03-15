import tornado.web
import tornado.template
import logging
from handlers.base_handler import BaseHandler

class InstructorHandler(BaseHandler):
    
    def get(self,id):
        
        instructor = self.application.settings['instructor'].get_item(id)
        logging.warn(instructor)
        if instructor is None: 
            #404 goes here
            return

        instructor_info_object = {
            "first_name" : instructor.get('instructor_first').title(),
            "last_name" : instructor.get('instructor_last').title(),
            "department" : instructor.get('department_id').upper(),
            # TODO
            "type" : instructor.get('instructor_group'),
            "sections" : len(instructor.get('fcqs')),
            "courses" : len(instructor.get('courses')),
            "last_fcq" : self.convert_date(instructor.get('fcqs_yearterms')[-1]),
            "first_fcq" : self.convert_date(instructor.get('fcqs_yearterms')[0]),
        }
        instructor_stats_object = {
            "effectiveness" : round(instructor.get('fcqs_stats').get('instructor_effectiveness_average'),2),
            "overall" : round(instructor.get('fcqs_stats').get('instructoroverall_average'),2),
            "availability" : round(instructor.get('fcqs_stats').get('instructor_availability_average'),2),
            "respect" : round(instructor.get('fcqs_stats').get('instructor_respect_average'),2),
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

        fcqs = self.get_fcq_data(instructor.get('fcqs'))

        self.render('layouts/instructor_view.html',
            instructor_info=instructor_info_object,
            instructor_stats=instructor_stats_object,
            department_info=department_info_object,
            instructor_fcqs=fcqs)
