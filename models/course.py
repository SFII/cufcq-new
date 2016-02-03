from models.basemodel import BaseModel


class Course(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']

    def requiredFields(self):
        return ['department_id', 'fcqs', 'instructors', 'course_number', 'course_subject', 'course_title', 'course_flavor', 'slug']

    def strictSchema(self):
        return False

    def fields(self):
        return {
            'campus': (self.is_in_list(CAMPUS_CODES), ),
            'department_id': (self.schema_or(self.is_none, self.exists_in_table('Department'), ),),
            'fcqs': (self.is_list, self.schema_list_check(self.is_string, )),
            'courses': (self.is_list, self.schema_list_check(self.is_string, )),
            'course_number': (self.is_int, self.is_truthy),
            'course_subject': (self.is_string, self.is_not_empty),
            'course_title': (self.is_string, self.is_not_empty),
            'course_flavor': (self.schema_or(self.is_none, self.is_string)),
            'slug': (self.string, self.is_not_empty, self.is_unique('slug')),
        }

    def default(self):
        return {
            'campus': '',
            'department_id': None,
            'fcqs': [],
            'instructors': [],
            'course_number': '',
            'course_title': '',
            'course_subject': '',
            'course_flavor': None,
            'slug': '',
        }

    def generate_slug(self, data):
        subject = data['subject']
        course_number = data['course_number']
        slug = "{0}-{1}".format(subject, course_number)
        return slug.lower()

    def sanitize_from_raw(self, raw):
        sanitized = self.default()
        sanitized['course_number'] = raw['course_number']
        sanitized['course_title'] = raw['course_title']
        sanitized['course_subject'] = raw['course_subject']
        sanitized['slug'] = self.generate_slug(sanitized)
        return sanitized

    def decompose_from_id(self, course_id):
        course_data = self.get_item(course_id)
        return self.decompose(course_data)

    def decompose(self, course_data):
        if course_data is None:
            return None
        decomposed_data = course_data.copy()
        decomposed_question_data = []
        question_ids = course_data['questions']
        for question_id in question_ids:
            question_data = Question().get_item(question_id)
            decomposed_question_data.append(question_data)
        decomposed_data['questions'] = decomposed_question_data
        return decomposed_data
