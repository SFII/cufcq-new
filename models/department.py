from models.basemodel import BaseModel


class Department(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']

    def requiredFields(self):
        return ['campus', 'fcqs', 'courses', 'instructors', 'slug', 'data']

    def strictSchema(self):
        return True

    def fields(self):
        return {
            'campus': (self.is_in_list(CAMPUS_CODES), ),
            'fcqs': (self.is_list, self.schema_list_check(self.exists_in_table('Fcq'))),  # TODO: exists_in_table is supposed to check for string components
            'courses': (self.is_list, self.schema_list_check(self.exists_in_table('Course'))),
            'instructors': (self.is_list, self.schema_list_check(self.exists_in_table('Instructor'))),
            'slug': (self.string, self.is_not_empty, self.is_unique('slug')),
            'data': (self.schema_or(self.is_none, self.is_list)),  # TODO: replace is_list with is_dict
        }

    def default(self):
        return {
            'campus': '',
            'fcqs': [],
            'courses': [],
            'instructors': [],
            'slug': '',
            'data': None
        }
