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


class Grade(BaseModel):

    def requiredFields(self):
        return ['denver_data', 'grade_data', 'campus', 'department_id', 'course_id', 'instructor_id', 'yearterm', 'course_number', 'course_subject', 'level', 'section', 'course_title', 'instructor_first', 'instructor_last', 'instructor_group', 'instructoroverall', 'courseoverall', 'forms_requested', 'forms_returned', 'id']

    def strictSchema(self):
        return False

    def fields(self):
        return {
            'department_id': (self.schema_or(self.is_none, self.exists_in_table('Department')),),
            'course_id': (self.schema_or(self.is_none, self.exists_in_table('Course')),),
            'instructor_id': (self.schema_or(self.is_none, self.exists_in_table('Instructor')),),
            'yearterm': (self.is_yearterm, ),
            'course_number': (self.is_int, self.is_truthy),
            'course_subject': (self.is_string, self.is_not_empty),
            'level': (self.is_in_list(self.COURSE_LEVELS), ),
            'section': (self.is_string, ),
            'course_title': (self.is_string, self.is_not_empty),
            'instructor_first': (self.is_string, self.is_not_empty, ),
            'instructor_last': (self.is_string, self.is_not_empty, ),
            'id': (self.is_string, self.is_not_empty, )
        }

    def generate_id(self, data):
        campus = data['campus']
        yearterm = data['yearterm']
        course_subject = data['course_subject']
        course_number = data['course_number']
        section = data['section']
        index = data['index_number']
        fcq_id = "{0}-{1}-{2}-{3}-{4}-{5}".format(campus, yearterm, course_subject, course_number, section, index)
        return fcq_id.lower()

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
            'index_number': 1,
            'fcq_department': '',
            'college': '',
            'asdiv': '',
            'activity_type': '',
            'level': '',
            'instruction_mode': None,
            'hours': '',
            'number_at_end_of_term': 0,
            'number_enrolled': 0,
            'number_graded': 0,
            'number_passed': 0,
            'number_nocredit': 0,
            'number_incomplete': 0,
            'percent_graded': 0.0,
            'average_grade': 0.0,
            'percent_a': 0.0,
            'percent_b': 0.0,
            'percent_c': 0.0,
            'percent_d': 0.0,
            'percent_f': 0.0,
            'percent_c_minus_or_below': 0.0,
            'percent_df': 0.0,
            'percent_dfw': 0.0,
            'percent_withdrawn': 0.0,
            'percent_incomplete': 0.0,
        }

    def sanitize_from_raw(self, raw):
        sanitized = self.default()
        sanitized['yearterm'] = int(raw['YearTerm'])
        sanitized['course_subject'] = raw['Subject'].replace(' ', '')
        sanitized['course_number'] = int(raw['Course'])
        sanitized['section'] = raw['Section']
        sanitized['campus'] = 'BD'
        sanitized['index_number'] = 1
        sanitized['fcq_department'] = raw['CrsPBADept']
        sanitized['college'] = raw['CrsPBAColl']
        sanitized['asdiv'] = raw['CrsPBADiv']
        sanitized['course_title'] = raw['CourseTitle'].capitalize()
        sanitized['level'] = {
            'Lower': 'LD',
            'Upper': 'UD'
        }.get(raw['Level'], 'GR')
        sanitized['activity_type'] = raw['Activity_Type']
        raw_instruction_mode = raw['Instruction_Mode']
        sanitized['instruction_mode'] = None if raw_instruction_mode == '' else raw_instruction_mode
        sanitized['hours'] = raw['Hours']
        sanitized['number_at_end_of_term'] = cast_to_int(raw['N_EOT'])
        sanitized['number_enrolled'] = cast_to_int(raw['N_ENROLL'])
        sanitized['number_graded'] = cast_to_int(raw['N_GRADE'])
        sanitized['percent_graded'] = cast_to_float(raw['PCT_GRADE'])
        sanitized['average_grade'] = cast_to_float(raw['AVG_GRD'])
        sanitized['percent_a'] = cast_to_float(raw['PCT_A'])
        sanitized['percent_b'] = cast_to_float(raw['PCT_B'])
        sanitized['percent_c'] = cast_to_float(raw['PCT_C'])
        sanitized['percent_d'] = cast_to_float(raw['PCT_D'])
        sanitized['percent_f'] = cast_to_float(raw['PCT_F'])
        sanitized['percent_c_minus_or_below'] = cast_to_float(raw['PCT_C_MINUS_OR_BELOW'])
        sanitized['percent_df'] = cast_to_float(raw['PCT_DF'])
        sanitized['percent_dfw'] = cast_to_float(raw['PCT_DFW'])
        sanitized['percent_withdrawn'] = cast_to_float(raw['PCT_WDRAW'])
        sanitized['percent_incomplete'] = cast_to_float(raw['PCT_INCOMP'])
        sanitized['number_passed'] = cast_to_int(raw['N_PASS'])
        sanitized['number_nocredit'] = cast_to_int(raw['N_NOCRED'])
        sanitized['number_incomplete'] = cast_to_int(raw['N_INCOMP'])
        instructor_names = raw['insname1'].split(',')
        if len(instructor_names) < 2:
            sanitized['instructor_last'] = instructor_names[0].strip()
            sanitized['instructor_first'] = instructor_names[0].strip().split(' ')[0]
        else:
            sanitized['instructor_last'] = instructor_names[0].strip()
            sanitized['instructor_first'] = instructor_names[1].strip().split(' ')[0]
        sanitized['rap'] = True if raw['RAP'] != '' else False
        sanitized['honors'] = raw['Honors']
        sanitized['id'] = self.generate_id(sanitized)
        d, c, i = self.generate_dci_ids(sanitized)
        sanitized['department_id'] = d
        sanitized['course_id'] = c
        sanitized['instructor_id'] = i
        return sanitized
