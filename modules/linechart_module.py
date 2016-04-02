from modules.chart_module import ChartModule
import tornado.web
import logging


class LineChartModule(ChartModule):

    def render(self, raw_data, keys, chart_id="linechart"):
        self.chart_id = chart_id
        self.chart_data = self.overtime_linechart_data(raw_data, keys)
        logging.warn(self.chart_data)
        return self.render_string('modules/linechart.html', chart_id=self.chart_id)

    def overtime_linechart_data(self, raw_data, keys):

        def _overtime_builder(overtime_data, key):
            def _transform_overtime_data(yearterm):
                return round(overtime_data[str(yearterm)][key], 1)
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
            }[key]
            label = {
                'course_howmuchlearned_average': 'Amount Learned',
                'course_challenge_average': 'Challenge',
                'courseoverall_average': 'Course Overall',
                'course_priorinterest_average': 'Prior Interest',
                'instructor_effectiveness_average': 'Effectiveness',
                'instructor_respect_average': 'Respect',
                'instructoroverall_average': 'Instructor Overall',
                'instructor_availability_average': 'Availability'
            }[key]
            return {
                'label': label,
                'backgroundColor': "rgba({0},{1},{2},0.2)".format(*color),
                'borderColor': "rgba({0},{1},{2},1)".format(*color),
                'pointBackgroundColor': "rgba({0},{1},{2},1)".format(*color),
                'pointHoverBackgroundColor': "rgba({0},{1},{2},1)".format(*color),
                'pointHoverBorderColor': "#fff",
                'pointHoverBorderWidth': 2,
                'pointHoverRadius': 5,
                'data': list(map(_overtime_builder(overtime_data, key), yearterms))
            }

        yearterms = raw_data['fcqs_yearterms']
        overtime_data = raw_data['fcqs_overtime']
        labels = list(map(self.convert_date, yearterms))
        datasets = list(map(_overtime_dataset_builder, keys))
        return tornado.escape.json_encode({
            'labels': labels,
            'datasets': datasets,
        })

    def chart_options(self):
        return super(LineChartModule, self).chart_options()

    def embedded_javascript(self):
        options = self.chart_options()
        foo = '''
        var ctx = document.getElementById("{2}").getContext("2d");
        var myLineChart = new Chart(ctx,{{
            type:'line',
            data:{1},
            options:{0}
        }});
        '''.format(options, self.chart_data, self.chart_id)
        logging.warn(foo)
        return foo
