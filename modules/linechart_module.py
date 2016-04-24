from modules.chart_module import ChartModule
import tornado.web
import logging


class LineChartModule(ChartModule):

    def render(self, raw_data, keys, chart_id="linechart"):
        self.chart_id = chart_id
        self.chart_data = self.overtime_linechart_data(raw_data, keys)
        return self.render_string('modules/linechart.html', chart_id=self.chart_id)

    def overtime_linechart_data(self, raw_data, keys,
                                yearterms_key='fcqs_yearterms',
                                overtime_key='fcqs_overtime'):

        def _overtime_builder(overtime_data, key):
            def _transform_overtime_data(yearterm):
                    value = overtime_data[str(yearterm)][key]
                    roundto = {
                        'percent_a': 3,
                        'percent_b': 3,
                        'percent_c': 3,
                        'percent_d': 3,
                        'percent_f': 3,
                        'percent_incomplete': 3,
                        'average_grade': 3
                    }.get(key, 1)
                    if value is not None:
                        return round(value, roundto)
                    else:
                        return None
            return _transform_overtime_data

        def _overtime_dataset_builder(key):
            color = {
                'course_howmuchlearned_average': (247, 92, 3),
                'course_challenge_average': (217, 3, 104),
                'courseoverall_average': (130, 2, 99),
                'course_priorinterest_average': (4, 167, 119),
                'instructor_effectiveness_average': (247, 92, 3),
                'instructor_respect_average': (217, 3, 104),
                'instructoroverall_average': (130, 2, 99),
                'instructor_availability_average': (4, 167, 119),
                'TTT_instructoroverall_average': (197, 27, 125),
                'OTH_instructoroverall_average': (233, 163, 201),
                'TA_instructoroverall_average': (253, 224, 239),
                'GR_courseoverall_average': (77, 146, 33),
                'UD_courseoverall_average': (161, 215, 106),
                'LD_courseoverall_average': (230, 245, 106),
                'percent_a': (44, 123, 182),
                'percent_b': (171, 217, 233),
                'percent_c': (255, 255, 191),
                'percent_d': (253, 174, 97),
                'percent_f': (215, 25, 28),
                'percent_incomplete': (48, 48, 48),
                'average_grade': (48, 48, 48),
            }.get(key, (48, 48, 48))
            yaxis_id = {
                'percent_a': 'y-axis-3',
                'percent_b': 'y-axis-3',
                'percent_c': 'y-axis-3',
                'percent_d': 'y-axis-3',
                'percent_f': 'y-axis-3',
                'percent_incomplete': 'y-axis-3',
                'average_grade': 'y-axis-2',
            }.get(key, 'y-axis-1')
            fill = {
                'percent_a': True,
                'percent_b': True,
                'percent_c': True,
                'percent_d': True,
                'percent_f': True,
                'percent_incomplete': True,
            }.get(key, False)
            label = {
                'course_howmuchlearned_average': 'Amount Learned',
                'course_challenge_average': 'Challenge',
                'courseoverall_average': 'Course Overall',
                'course_priorinterest_average': 'Prior Interest',
                'instructor_effectiveness_average': 'Effectiveness',
                'instructor_respect_average': 'Respect',
                'instructoroverall_average': 'Instructor Overall',
                'instructor_availability_average': 'Availability',
                'TTT_instructoroverall_average': 'TTT instructors',
                'OTH_instructoroverall_average': 'OTH instructors',
                'TA_instructoroverall_average': 'TA instructors',
                'GR_courseoverall_average': 'GR Course Overall',
                'UD_courseoverall_average': 'UD Course Overall',
                'LD_courseoverall_average': 'LD Course Overall',
                'percent_a': 'A Grade',
                'percent_b': 'B Grade',
                'percent_c': 'C Grade',
                'percent_d': 'D Grade',
                'percent_f': 'F Grade',
                'percent_incomplete': 'Incomplete',
                'average_grade': 'Average GPA'
            }.get(key, '???')
            background_alpha = 1.0 if fill else 0.2
            return {
                'label': label,
                'fill': fill,
                'yAxisID': yaxis_id,
                'backgroundColor': "rgba({0},{1},{2},{background_alpha})".format(*color, background_alpha=background_alpha),
                'borderColor': "rgba({0},{1},{2},1)".format(*color),
                'pointBackgroundColor': "rgba({0},{1},{2},1)".format(*color),
                'pointHoverBackgroundColor': "rgba({0},{1},{2},1)".format(*color),
                'pointHoverBorderColor': "#fff",
                'pointHoverBorderWidth': 2,
                'pointHoverRadius': 5,
                'data': list(map(_overtime_builder(overtime_data, key), yearterms))
            }

        yearterms = raw_data[yearterms_key]
        overtime_data = raw_data[overtime_key]
        labels = list(map(self.convert_date, yearterms))
        datasets = list(map(_overtime_dataset_builder, keys))
        return tornado.escape.json_encode({
            'labels': labels,
            'datasets': datasets,
        })

    def embedded_javascript(self):
        options = tornado.escape.json_encode(self.chart_options())
        foo = '''
        new Chart(document.getElementById("{2}").getContext("2d"),{{
            type:'line',
            data:{1},
            options:{0}
        }});
        '''.format(options, self.chart_data, self.chart_id)
        return foo
