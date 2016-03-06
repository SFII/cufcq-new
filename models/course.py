from models.basemodel import BaseModel


class Course(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']
    COURSE_LEVELS = ['GR', 'LD', 'UD']

    def requiredFields(self):
        return ['department_id', 'fcqs', 'alternate_titles', 'instructors', 'course_number', 'course_subject', 'course_title', 'course_flavor', 'id', 'level']

    def strictSchema(self):
        return False

    def fields(self):
        return {
            'campus': (self.is_in_list(self.CAMPUS_CODES), ),
            'level': (self.is_in_list(self.COURSE_LEVELS), ),
            'department_id': (self.schema_or(self.is_none, self.is_string, ),),
            'fcqs': (self.is_list, self.schema_list_check(self.is_string, ),),
            'grades': (self.is_list, self.schema_list_check(self.is_string, ),),
            'courses': (self.is_list, self.schema_list_check(self.is_string, ),),
            'course_number': (self.is_int, self.is_truthy),
            'course_subject': (self.is_string, self.is_not_empty, ),
            'course_title': (self.is_string, self.is_not_empty, ),
            'course_flavor': (self.schema_or(self.is_none, self.is_string),),
            'id': (self.is_string, self.is_not_empty, ),
        }

    def default(self):
        return {
            'campus': '',
            'department_id': None,
            'alternate_titles': [],
            'fcqs': [],
            'grades': [],
            'instructors': [],
            'course_number': '',
            'course_title': '',
            'course_subject': '',
            'course_flavor': None,
            'id': '',
        }

    def generate_id(self, data):
        campus = data['campus']
        course_subject = data['course_subject']
        course_number = data['course_number']
        course_id = "{0}-{1}-{2}".format(campus, course_subject, course_number)
        return course_id.lower()

    def sanitize_from_raw(self, raw):
        sanitized = self.default()
        sanitized['department_id'] = raw['department_id']
        sanitized['campus'] = raw['campus']
        sanitized['course_number'] = raw['course_number']
        sanitized['course_title'] = raw['course_title']
        sanitized['course_subject'] = raw['course_subject']
        sanitized['level'] = raw['level']
        sanitized['id'] = self.generate_id(sanitized)
        return sanitized
