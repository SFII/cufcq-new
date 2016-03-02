from models.basemodel import BaseModel


class Instructor(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']

    def requiredFields(self):
        return ['fcqs', 'courses', 'yearterms', 'overtime', 'stats', 'instructor_first', 'instructor_last', 'department_id', 'id']

    def strictSchema(self):
        return False

    def fields(self):
        return {
            'department_id': (self.schema_or(self.is_none, self.is_string, ),),
            'fcqs': (self.is_list, self.schema_list_check(self.is_string, )),
            'fcq_yearterms': (self.is_list, self.schema_list_check(self.is_int, )),
            'grade_yearterms': (self.is_list, self.schema_list_check(self.is_int, )),
            'courses': (self.is_list, self.schema_list_check(self.is_string, )),
            'instructor_first': (self.is_string, self.is_not_empty, ),
            'instructor_last': (self.is_string, self.is_not_empty, ),
            'id': (self.is_string, self.is_not_empty, ),
        }

    def default(self):
        return {
            'department_id': None,
            'fcqs': [],
            'grades': [],
            'yearterms': [],
            'overtime': {},
            'stats': {},
            'courses': [],
            'yearterms': [],
            'instructor_first': '',
            'instructor_last': '',
            'id': '',
        }

    def generate_id(self, data):
        instructor_last = data['instructor_last']
        instructor_first = data['instructor_first']
        instructor_id = "{0}-{1}".format(instructor_last, instructor_first).replace(' ', '')
        return instructor_id.lower()

    def sanitize_from_raw(self, raw):
        sanitized = self.default()
        sanitized['department_id'] = raw['department_id']
        sanitized['instructor_first'] = raw['instructor_first']
        sanitized['instructor_last'] = raw['instructor_last']
        sanitized['id'] = self.generate_id(sanitized)
        return sanitized
