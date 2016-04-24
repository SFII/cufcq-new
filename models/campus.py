from models.basemodel import BaseModel


class Campus(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']
    LONG_NAMES = {
        'BD': 'University of Colorado, Boulder',
        'DN': 'University of Colorado, Denver',
        'CS': 'University of Colorado, Colorado Springs'
    }

    def requiredFields(self):
        return ['campus', 'fcqs', 'courses', 'instructors', 'departments', 'colleges', 'id']

    def fields(self):
        return {
            'campus': (self.is_in_list(self.CAMPUS_CODES), ),
            'fcqs': (self.is_list, self.schema_list_check(self.is_string, )),
            'grades': (self.is_list, self.schema_list_check(self.is_string, ),),
            'courses': (self.is_list, self.schema_list_check(self.is_string, )),
            'instructors': (self.is_list, self.schema_list_check(self.is_string, )),
            'departments': (self.is_list, self.schema_list_check(self.is_string, )),
            'colleges': (self.is_list, self.schema_list_check(self.is_string, )),
            'id': (self.is_string, self.is_not_empty, ),
        }

    def default(self):
        return {
            'campus': '',
            'fcqs': [],
            'grades': [],
            'courses': [],
            'instructors': [],
            'departments': [],
            'colleges': [],
            'id': '',
        }
