from models.basemodel import BaseModel


class Fcq(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']
    VALID_TERMS = {1: 'Spring', 4: 'Summer', 7: 'Fall'}
    VALID_GROUPS = ['TA', 'TTT', 'OTH']

    def requiredFields(self):
        return ['campus', 'department_id', 'course_id', 'instructor_id', 'yearterm', 'course_number', 'course_subject', 'course_title', 'instructor_first', 'instructor_last', 'slug']

    def strictSchema(self):
        return False

    def fields(self):
        return {
            'campus': (self.is_string, self.is_not_empty, self.is_in_list(CAMPUS_CODES), ),
            'department_id': (self.schema_or(self.is_none, self.exists_in_table('Department'))),
            'course_id': (self.schema_or(self.is_none, self.exists_in_table('Course'))),
            'instructor_id': (self.schema_or(self.is_none, self.exists_in_table('Instructor'))),
            'yearterm': (self.is_yearterm),
            'course_number': (self.is_int, self.is_truthy),  # TODO: is_unique('course_number', scope=['course_subject'])
            'course_subject': (self.is_string, self.is_not_empty),
            'course_title': (self.is_string, self.is_not_empty),
            'instructor_first': (self.string, self.is_not_empty, ),  # TODO self.is_unique('instructor_first', scope=['instructor_last'])
            'instructor_last': (self.string, self.is_not_empty, ),
            'slug': (self.string, self.is_not_empty, self.is_unique('slug'))
        }

    def is_yearterm(self, data):
        self.is_int(data)
        key = data % 10
        assert key in VALID_TERMS.keys

    def default(self):
        return {
            'campus': '',
            'department_id': None,
            'course_id': None,
            'instructor_id': None,
            'yearterm': 0,
            'course_number': 0,
            'course_subject': '',
            'course_title': '',
            'instructor_first': '',
            'instructor_last': '',
            'slug': ''
        }
