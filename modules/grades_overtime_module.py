from modules.chart_module import ChartModule
import tornado.web
import logging


class GradesOvertimeModule(ChartModule):

    def render(self, overtime_data, yearterms_data):
        return self.render_string('modules/grades_overtime_chart.html',
                                  grades_overtime=overtime_data,
                                  grades_yearterms=yearterms_data)

    def javascript_files(self):
        return ["js/charts/grades_overtime_chart.js"]
