from handlers.base_handler import BaseHandler


class DepartmentHandler(BaseHandler):
    
    def color(self):
        return 'violet'

    def get(self, id):
        department = self.application.settings['department'].get_item(id)
        if department is None:
            self.redirect('/notFound')
            return

        department_info_object = {
            "long_name": department.get('long_name').title(),
            "code": department.get('name'),
            "campus": self.convert_campus(department.get('campus')),
            "college": department.get('college'),
            "instructors": len(department.get('instructors')),
            "courses": len(department.get('courses')),
            "first_fcq": self.convert_date(department.get('fcqs_yearterms')[0]),
            "last_fcq": self.convert_date(department.get('fcqs_yearterms')[-1]),
        }

        department_stats_object = {
            "course_overall": round(
                department.get('fcqs_stats').get('courseoverall_average'), 1),
            "instructor_overall": round(
                department.get('fcqs_stats').get('instructoroverall_average'), 1),
            "course_challenge": round(
                department.get('fcqs_stats').get('course_challenge_average'), 1),
            "course_learned": round(
                department.get('fcqs_stats').get('course_howmuchlearned_average'), 1),
        }


        self.render('layouts/department_view.html',
                    department_info=department_info_object,
                    department_stats=department_stats_object,)
