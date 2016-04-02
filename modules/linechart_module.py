from modules.chart_module import ChartModule
import tornado.web
import logging


class LineChartModule(ChartModule):

    def render(self, header, color, chart_data, chart_id="linechart"):
        self.chart_id = chart_id
        self.chart_data = chart_data
        return self.render_string('modules/linechart.html',
                                  header=header, color=color, chart_id=self.chart_id)

    def embedded_javascript(self):
        return '''
        var options = {0};
        var data = {1};
        var ctx = document.getElementById("{2}").getContext("2d");
        var myLineChart = new Chart(ctx).Line(data, options);
        '''.format(self.chart_options, self.chart_data, self.chart_id)
