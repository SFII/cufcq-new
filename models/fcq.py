from models.basemodel import BaseModel


def cast_to_float(string):
    try:
        return float(string)
    except:
        return None


def cast_to_int(string):
    try:
        return int(string)
    except:
        return 0


class Fcq(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']
    VALID_TERMS = {1: 'Spring', 4: 'Summer', 7: 'Fall'}
    INSTRUCTOR_GROUPS = ['TA', 'TTT', 'OTH']
    COURSE_LEVELS = ['GR', 'LD', 'UD']

    def requiredFields(self):
        return ['denver_data', 'campus', 'department_id', 'course_id', 'instructor_id', 'yearterm', 'course_number', 'course_subject', 'level', 'section', 'course_title', 'instructor_first', 'instructor_last', 'instructor_group', 'instructoroverall', 'courseoverall', 'forms_requested', 'forms_returned', 'id']

    def strictSchema(self):
        return False

    def fields(self):
        return {
            'campus': (self.is_in_list(self.CAMPUS_CODES), ),
            'department_id': (self.schema_or(self.is_none, self.exists_in_table('Department')),),
            'course_id': (self.schema_or(self.is_none, self.exists_in_table('Course')),),
            'instructor_id': (self.schema_or(self.is_none, self.exists_in_table('Instructor')),),
            'yearterm': (self.is_yearterm, ),
            'course_number': (self.is_int, self.is_truthy),
            'course_subject': (self.is_string, self.is_not_empty),
            'level': (self.is_in_list(self.COURSE_LEVELS), ),
            'section': (self.is_string, ),
            'course_title': (self.is_string, self.is_not_empty),
            'instructor_first': (self.is_string, ),
            'instructor_last': (self.is_string, self.is_not_empty, ),
            'instructor_group': (self.is_in_list(self.INSTRUCTOR_GROUPS), ),
            'forms_requested': (self.is_int, self.is_truthy),
            'forms_returned': (self.is_int, ),
            'courseoverall': (self.schema_or(self.is_none, self.is_fcq_value),),
            'instructoroverall': (self.schema_or(self.is_none, self.is_fcq_value),),
            'id': (self.is_string, self.is_not_empty, )
        }

    def is_yearterm(self, data):
        self.is_int(data)
        key = data % 10
        assert key in [1, 4, 7]

    def is_fcq_value(self, data):
        self.is_int(data)
        self.is_in_range(1.0, 6.0)(data)

    def generate_id(self, data):
        campus = data['campus']
        yearterm = data['yearterm']
        course_subject = data['course_subject']
        course_number = data['course_number']
        section = data['section']
        index = data['index_number']
        fcq_id = "{0}-{1}-{2}-{3}-{4}-{5}".format(campus, yearterm, course_subject, course_number, section, index)
        return fcq_id.lower()

    def generate_denver_data(self, raw, campus, yearterm):
        if campus == 'DN' and yearterm <= 20144:
            return {
                'r_fairness': cast_to_float(raw['R_Fair']),
                'r_presentation': cast_to_float(raw['R_Presnt']),
                'r_workload': cast_to_float(raw['Workload']),
                'r_diversity': cast_to_float(raw['R_Divstu']),
                'r_accessibility': cast_to_float(raw['R_Access']),
                'r_learning': cast_to_float(raw['R_Learn'])
            }
        return None

    def generate_dci_ids(self, data):
        campus = data['campus']
        course_subject = data['course_subject']
        course_number = data['course_number']
        instructor_last = data['instructor_last']
        instructor_first = data['instructor_first']
        department_id = "{0}-{1}".format(campus, course_subject).lower()
        course_id = "{0}-{1}-{2}".format(campus, course_subject, course_number).lower()
        instructor_id = "{0}-{1}".format(instructor_last, instructor_first).lower().replace(' ', '')
        return (department_id, course_id, instructor_id,)

    def default(self):
        return {
            'denver_data': None,
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
            'instructor_group': '',
            'courseoverall': None,
            'instructoroverall': None,
            'forms_requested': 0,
            'forms_returned': 0,
            'id': ''
        }

    def sanitize_from_raw(self, raw):
        sanitized = self.default()
        sanitized['yearterm'] = int(raw['Yearterm'])
        sanitized['campus'] = raw['Campus']
        sanitized['course_subject'] = raw['Subject'].replace(' ', '')
        sanitized['course_number'] = int(raw['Crse'])
        sanitized['course_title'] = raw['CrsTitle'].capitalize()
        sanitized['section'] = raw['Sec']
        sanitized['online_fcq'] = True if len(raw['OnlineFCQ']) else False
        sanitized['bd_continuing_education'] = True if len(raw['BDContinEdCrse']) else False
        instructor_names = raw['Instructor'].split(',')
        if len(instructor_names) < 2:
            sanitized['instructor_last'] = instructor_names[0].strip()
            sanitized['instructor_first'] = instructor_names[0].strip()
        else:
            sanitized['instructor_last'] = instructor_names[0].strip()
            sanitized['instructor_first'] = instructor_names[1].strip()
        sanitized['instructor_last'].replace(' ', '-').replace('/', '-')
        sanitized['instructor_first'].replace(' ', '-').replace('/', '-')
        sanitized['instructor_group'] = raw.get('Instr_Group', 'TTT')
        sanitized['forms_requested'] = cast_to_int(raw['FormsRequested'])
        sanitized['forms_returned'] = cast_to_int(raw['FormsReturned'])
        sanitized['courseoverall_pct_valid'] = cast_to_float(raw['CourseOverallPctValid'])
        sanitized['courseoverall'] = cast_to_float(raw['CourseOverall'])
        sanitized['courseoverall_sd'] = cast_to_float(raw['CourseOverall_SD'])
        sanitized['instructoroverall'] = cast_to_float(raw['InstructorOverall'])
        sanitized['instructoroverall_sd'] = cast_to_float(raw['InstructorOverall_SD'])
        sanitized['hours_per_week_in_class_string'] = raw['HoursPerWkInclClass']
        # Instructor Data
        sanitized['instructor_effectiveness'] = cast_to_float(raw['InstrEffective'])
        sanitized['instructor_availability'] = cast_to_float(raw['Availability'])
        sanitized['instructor_respect'] = cast_to_float(raw['InstrRespect'])
        # Course Data
        sanitized['course_challenge'] = cast_to_float(raw['Challenge'])
        sanitized['course_howmuchlearned'] = cast_to_float(raw['HowMuchLearned'])
        sanitized['course_priorinterest'] = cast_to_float(raw['PriorInterest'])
        sanitized['denver_data'] = self.generate_denver_data(raw, sanitized['campus'], sanitized['yearterm'])
        sanitized['college'] = raw['College']
        sanitized['asdiv'] = raw['ASdiv']
        sanitized['level'] = raw['Level']
        sanitized['fcq_department'] = raw['Fcqdept']
        sanitized['index_number'] = int(raw['I_Num'])
        sanitized['id'] = self.generate_id(sanitized)
        d, c, i = self.generate_dci_ids(sanitized)
        sanitized['department_id'] = d
        sanitized['course_id'] = c
        sanitized['instructor_id'] = i
        return sanitized
