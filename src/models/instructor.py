from models.basemodel import BaseModel


class Instructor(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']

    def requiredFields(self):
        return ['campus', 'fcqs', 'courses', 'instructor_first', 'instructor_last', 'slug', 'data']

    def strictSchema(self):
        return True

    def fields(self):
        return {
            'campus': (self.is_string, self.is_not_empty, self.is_in_list(CAMPUS_CODES), ),
            'department_id': (self.is_string, self.is_not_empty, self.exists_in_table('Department')),
            'fcqs': (self.is_list, self.is_not_empty, self.schema_list_check(self.is_string, self.exists_in_table('Fcq'))),
            'courses': (self.is_list, self.is_not_empty, self.schema_list_check(self.is_string)),
            'instructor_first': (self.string, self.is_not_empty, ),  # TODO self.is_unique('instructor_first', scope=['instructor_last'])
            'instructor_last': (self.string, self.is_not_empty, ),
            'slug': (self.string, self.is_not_empty, self.is_unique('slug')),
            'data': (self.schema_or(self.is_none, self.is_list)),  # TODO: replace is_list with is_dict
        }

    def default(self):
        return {
            'campus': '',
            'department_id': '',
            'fcqs': [],
            'courses': [],
            'instructor_first': '',
            'instructor_last': '',
            'slug': '',
            'data': None
        }

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
