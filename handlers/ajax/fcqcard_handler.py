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
        course_level = self.convert_level(fcq_data['level'])
        denver_data = fcq_data['denver_data']
        date = self.convert_date(fcq_data['yearterm'])
        campus = self.convert_campus(fcq_data['campus'])
        chart_options = tornado.escape.json_encode({
            'legend': {
                'display': False,
            },
            'title': {
                'display': False,
            },
        })
        gradepie_json = tornado.escape.json_encode([])
        if grade_data:
            gradepie_data = {
                'labels': [
                    'A Grade',
                    'B Grade',
                    'C Grade',
                    'D Grade',
                    'F Grade',
                    'Incomplete'
                ],
                'datasets': [{
                    'data': [
                        round(100 * grade_data['percent_a'], 0),
                        round(100 * grade_data['percent_b'], 0),
                        round(100 * grade_data['percent_c'], 0),
                        round(100 * grade_data['percent_d'], 0),
                        round(100 * grade_data['percent_f'], 0),
                        round(100 * grade_data['percent_incomplete'], 0)
                    ],
                    'backgroundColor': [
                        '#2c7bb6',
                        '#abd9e9',
                        '#ffffbf',
                        '#fdae61',
                        '#d7191c',
                        '#333333'
                    ]
                }]
            }
            gradepie_json = tornado.escape.json_encode(gradepie_data)

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

        def saferound(value, roundto=1):
            if value is None:
                return 'n/a'
            return round(value, roundto)

        def disabled(value):
            if not value:
                return "disabled"
            return ""

        return self.render('modules/fcqdata.html',
                           saferound=saferound,
                           gradepie_json=gradepie_json,
                           chart_options=chart_options,
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
