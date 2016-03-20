import tornado.web
import tornado.template
from handlers.base_handler import BaseHandler
import logging


class FcqCardHandler(BaseHandler):
    def get(self, item_id):
        fcq_data = self.application.settings['fcq'].get_item(item_id)
        grade_data = self.application.settings['grade'].get_item(item_id)
        fcq_id = item_id
        instructor_group = {
            'TTT': "<abbr title=\"Tenured or tenure-track instructor\">TTT</abbr>",
            'OTH': "<abbr title=\"Other primary instructor, such as adjunct, visiting, honorarium, etc.\">OTH</abbr>",
            'TA': "<abbr title=\"Teaching Assistant\">TA</abbr>"
        }[fcq_data['instructor_group']]
        course_level = {
            'GR': "Graduate Level",
            'UD': "Upper Division",
            'LD': "Lower Division"
        }[fcq_data['level']]
        denver_data = fcq_data['denver_data']
        date = self.convert_date(fcq_data['yearterm'])
        campus = self.convert_campus(fcq_data['campus'])

        def progress_bar(numerator, denominator):
            numer = numerator or 0
            denom = denominator or 1
            percentage = int(100 * (numer / float(denom)))
            color = "progress-bar-primary"
            if percentage < 20:
                color = "progress-bar-danger"
            if percentage < 50:
                color = "progress-bar-warning"
            return '''
            <div class="progress progress-hairline">
            <div class="progress-bar {0}"
            style="width:{1}%"></div>
            </div>
            '''.format(color, percentage)

        def saferound(value):
            val = value or -1.0
            if val < 0:
                return 'n/a'
            return round(val, 1)

        def disabled(value):
            if not value:
                return "disabled"
            return ""

        return self.render('modules/fcqdata.html',
                           saferound=saferound,
                           instructor_group=instructor_group,
                           course_level=course_level,
                           disabled=disabled,
                           progress_bar=progress_bar,
                           fcq_id=fcq_id,
                           fcq_data=fcq_data,
                           grade_data=grade_data,
                           denver_data=denver_data,
                           date=date,
                           campus=campus)
