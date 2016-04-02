from modules.chart_module import ChartModule
import tornado.web
import logging


class LineChartModule(ChartModule):

    def render(self, header, color, chart_data, chart_id="linechart"):
        self.chart_id = chart_id
        self.chart_data = chart_data
        return self.render_string('modules/linechart.html',
                                  header=header, color=color, chart_id=self.chart_id)
    def chart_options(self):
        return super(LineChartModule, self).chart_options()

    def embedded_javascript(self):
        options = self.chart_options()
        return '''
        var ctx = document.getElementById("{2}").getContext("2d");
        var myLineChart = new Chart(ctx,{{
            type:'line',
            data:{1},
            options:{0}
        }});
        '''.format(options, self.chart_data, self.chart_id)
