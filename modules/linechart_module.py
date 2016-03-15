from modules.chart_module import ChartModule
import tornado.web
import logging


class LineChartModule(ChartModule):

    def render(self, header, chart_data):
        self.chart_data = chart_data
        return '''
        <div class="col-md-8">
          <div class="card-head">
            <header>{0}</header>
          </div>
          <div class="card-body height-8">
              <canvas id="{1}" width="auto" height="auto">
          </div>
        </div>
        '''.format(header, self.chart_id)

    def embedded_javascript(self):
        return '''
        var options = {0};
        var data = {1};
        var ctx = document.getElementById("{2}").getContext("2d");
        var myLineChart = new Chart(ctx).Line(data, options);
        '''.format(self.chart_options, self.chart_data, self.chart_id)
