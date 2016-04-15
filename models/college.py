from models.basemodel import BaseModel


class College(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']
    LONG_NAMES = {
        'AS': 'College of Arts and Sciences',
        "AM": 'College of Arts and Media',
        "AP": 'College of Architecture and Planning',
        "BD": 'Business School',
        "BU": 'Leeds School of Business',
        "EB": 'School of Education',
        "EC": 'College of Education',
        "ED": 'School of Education',
        "EN": 'College of Engineering and Applied Sciences',
        "EP": 'School of Education and Human Development',
        "ES": 'College of Engineering and Applied Science',
        "EV": 'Program in Environmental Design',
        "JR": 'Journalism (discontinued)',
        "LA": 'College of Liberal Arts and Sciences',
        "LS": 'College of Letters, Arts, and Sciences',
        "LW": 'Law School',
        "MB": 'College of Music',
        "MC": 'College of Media, Communication and Information',
        "NR": 'College of Nursing and Health Sciences',
        "PA": 'School of Public Affairs',
        "UH": '(unofficial) Military Sciences',
        "XX": '(unofficial) Military Sciences',
        "XY": 'Interdisciplinary Innovation'
    }

    def requiredFields(self):
        return ['campus', 'name', 'fcqs', 'courses', 'instructors', 'departments', 'id']

    def fields(self):
        return {
            'campus': (self.is_in_list(self.CAMPUS_CODES), ),
            'name': (self.is_string, self.is_not_empty, ),
            'fcqs': (self.is_list, self.schema_list_check(self.is_string, )),
            'grades': (self.is_list, self.schema_list_check(self.is_string, ),),
            'courses': (self.is_list, self.schema_list_check(self.is_string, )),
            'instructors': (self.is_list, self.schema_list_check(self.is_string, )),
            'departments': (self.is_list, self.schema_list_check(self.is_string, )),
            'id': (self.is_string, self.is_not_empty, ),
        }

    def default(self):
        return {
            'campus': '',
            'name': '',
            'fcqs': [],
            'grades': [],
            'courses': [],
            'instructors': [],
            'departments': [],
            'id': '',
        }
