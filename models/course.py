from models.basemodel import BaseModel
import rethinkdb as r

class Course(BaseModel):
    CAMPUS_CODES = ['BD', 'DN', 'CS']
    COURSE_LEVELS = ['GR', 'LD', 'UD']

    def requiredFields(self):
        return ['department_id', 'fcqs', 'alternate_titles', 'yearterms', 'overtime', 'stats', 'instructors', 'course_number', 'course_subject', 'course_title', 'course_flavor', 'id', 'level']

    def strictSchema(self):
        return False

    def fields(self):
        return {
            'campus': (self.is_in_list(self.CAMPUS_CODES), ),
            'level': (self.is_in_list(self.COURSE_LEVELS), ),
            'department_id': (self.schema_or(self.is_none, self.is_string, ),),
            'fcqs': (self.is_list, self.schema_list_check(self.is_string, ),),
            'yearterms': (self.is_list, self.schema_list_check(self.is_int, )),
            'courses': (self.is_list, self.schema_list_check(self.is_string, ),),
            'course_number': (self.is_int, self.is_truthy),
            'course_subject': (self.is_string, self.is_not_empty, ),
            'course_title': (self.is_string, self.is_not_empty, ),
            'course_flavor': (self.schema_or(self.is_none, self.is_string),),
            'id': (self.is_string, self.is_not_empty, ),
        }

    def default(self):
        return {
            'campus': '',
            'department_id': None,
            'alternate_titles': [],
            'fcqs': [],
            'yearterms': [],
            'overtime': {},
            'stats': {},
            'instructors': [],
            'course_number': '',
            'course_title': '',
            'course_subject': '',
            'course_flavor': None,
            'id': '',
        }

    def search_items(self, searchstring, returnfields=['id']):
        """
        Searches through the Table
        1) search all alternate_titles for full searchstring
        2) if searchstring contains a number > 99, search course_numbers for that number
        3) if searchstring contains a ngram with four or fewer characters, looks through course_subject
        """
        table = 'Course'
        searchstring.replace('-', ' ')
        words = searchstring.split(' ')
        subject_words = list(filter(lambda x: 2 <= len(x) <= 4), words)
        numbers = list(map(lambda x: int(x), filter(lambda x: x.isdigit(), words)))
        course_numbers = list(filter(lambda x: 100 <= x <= 9999, numbers))
        for course_number in course_numbers:
            try:
                words.remove(str(course_numbers))
            except:
                "do nothing, fail quietly"
        for subject_word in subject_words:
            try:
                words.remove(str(subject_word))
            except:
                "do nothing, fail quietly"
        title_results = r.expr(words).map(
            lambda word: r.db(DB).table(table).filter(
                lambda doc: doc['alternate_titles'].map(
                    lambda title: title.do(
                        lambda matcher: matcher.match('(?i)' + word)
                    )
                ).reduce(lambda left, right: left | right)
            )
        ).pluck('id').coerce_to('array')
        subject_results = r.expr(subject_words).map(
            lambda subject: r.db(DB).table(table).filter(
                lambda doc: doc['course_subject'] == subject
            )
        ).pluck('id').coerce_to('array')
        number_results = r.expr(course_numbers).map(
            lambda number: r.db(DB).table(table).filter(
                lambda doc: doc['course_number'] == number
            )
        ).pluck('id').coerce_to('array')

        searchresults = (r.expr(title_results) + number_results + subject_results).do(
            lambda bunch: r.add(r.args(bunch.map(
                lambda item: item['id']
            )))
        ).group(r.row).count().ungroup().orderBy('reduction')

        best_score = searchresults[-1]['reduction']

        best_ids = r.expr(searchresults).filter({'reduction': best_score}).get_field('group')

        if 'id' not in returnfields:
            logging.warn("'id' is not in listed returnfields. It's recomended this field is amongst those returned")
        if not len(returnfields):
            logging.error("returnfields cannot be empty")
            return []
        table = self.__class__.__name__
        try:
            return r.db(DB).table(table).filter(
                lambda doc: doc['course_title'].match(searchstring)
            ).pluck(r.args(searchfields)).run(conn)
        except:
            return []

    def generate_id(self, data):
        campus = data['campus']
        course_subject = data['course_subject']
        course_number = data['course_number']
        course_id = "{0}-{1}-{2}".format(campus, course_subject, course_number)
        return course_id.lower()

    def sanitize_from_raw(self, raw):
        sanitized = self.default()
        sanitized['department_id'] = raw['department_id']
        sanitized['campus'] = raw['campus']
        sanitized['course_number'] = raw['course_number']
        sanitized['course_title'] = raw['course_title']
        sanitized['course_subject'] = raw['course_subject']
        sanitized['level'] = raw['level']
        sanitized['id'] = self.generate_id(sanitized)
        return sanitized
