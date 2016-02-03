from models.basemodel import BaseModel


class Instructor(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']

    def requiredFields(self):
        return ['fcqs', 'courses', 'instructor_first', 'instructor_last', 'department_id', 'slug', 'data']

    def strictSchema(self):
        return False

    def fields(self):
        return {
            'department_id': (self.schema_or(self.is_none, self.exists_in_table('Department'), ),),
            'fcqs': (self.is_list, self.schema_list_check(self.is_string, )),
            'courses': (self.is_list, self.schema_list_check(self.is_string, )),
            'instructor_first': (self.string, self.is_not_empty, ),
            'instructor_last': (self.string, self.is_not_empty, ),
            'slug': (self.string, self.is_not_empty, self.is_unique('slug')),
        }

    def default(self):
        return {
            'department_id': None,
            'fcqs': [],
            'courses': [],
            'instructor_first': '',
            'instructor_last': '',
            'slug': '',
        }

    def generate_slug(self, data):
        instructor_last = data['instructor_last']
        instructor_first = data['instructor_first']
        slug = "{0}-{1}".format(instructor_last, instructor_first)
        return slug.lower()

    def sanitize_from_raw(self, raw):
        sanitized = self.default()
        sanitized['instructor_first'] = raw['instructor_first']
        sanitized['instructor_last'] = raw['instructor_last']
        sanitized['slug'] = self.generate_slug(sanitized)
        return sanitized

    def decompose_from_id(self, instructor_id):
        instructor_data = self.get_item(instructor_id)
        return self.decompose(instructor_data)

    def decompose(self, instructor_data):
        if instructor_data is None:
            return None
        decomposed_data = instructor_data.copy()
        decomposed_question_data = []
        question_ids = instructor_data['questions']
        for question_id in question_ids:
            question_data = Question().get_item(question_id)
            decomposed_question_data.append(question_data)
        decomposed_data['questions'] = decomposed_question_data
        return decomposed_data
