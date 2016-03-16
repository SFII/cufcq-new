from tornado.web import UIModule


class BaseModule(UIModule):
    def convert_date(self, yearterm):
        VALID_TERMS = {'1': 'Spring', '4': 'Summer', '7': 'Fall'}
        yearterm_str = str(yearterm)
        year = yearterm_str[0:4]
        term = VALID_TERMS.get(yearterm_str[4])
        return '{0} {1}'.format(term, year)

    def convert_campus(self, campus):
        return {
            'BD': 'Boulder',
            'DN': 'Denver',
            'CS': 'Colorado Springs'
        }[campus.upper()]

    def fcq_title(self, fcq_id):
        fcq_parts = fcq_id.split('-')
        date = self.convert_date(fcq_parts[1])
        campus = self.convert_campus(fcq_parts[0])
        course = "{0}-{1}-{2}".format(fcq_parts[2], fcq_parts[3], fcq_parts[4])
        return "{0} {1} {2}".format(campus, date, course)

    def render(self):
        return '''
        '''
