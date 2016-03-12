from modules.base_module import BaseModule
import tornado.web
import logging


class ChartOvertimeModule(BaseModule):
    chart_data = {}
    chart_options = tornado.escape.json_encode({
        #  Boolean - whether or not the chart should be responsive and resize when the browser does.
        'responsive': True,
        # /Boolean - Whether grid lines are shown across the chart
        'scaleShowGridLines': True,
        # String - Colour of the grid lines
        'scaleGridLineColor': "rgba(0,0,0,.05)",
        # Number - Width of the grid lines
        'scaleGridLineWidth': 1,
        # Boolean - Whether to show horizontal lines (except X axis)
        'scaleShowHorizontalLines': True,
        # Boolean - Whether to show vertical lines (except Y axis)
        'scaleShowVerticalLines': True,
        # Boolean - Whether the line is curved between points
        'bezierCurve': True,
        # Number - Tension of the bezier curve between points
        'bezierCurveTension': 0.4,
        # Boolean - Whether to show a dot for each point
        'pointDot': True,
        # Number - Radius of each point dot in pixels
        'pointDotRadius': 2,
        # Number - Pixel width of point dot stroke
        'pointDotStrokeWidth': 1,
        # Number - amount extra to add to the radius to cater for hit detection outside the drawn point
        'pointHitDetectionRadius': 20,
        # Boolean - Whether to show a stroke for datasets
        'datasetStroke': True,
        # Number - Pixel width of dataset stroke
        'datasetStrokeWidth': 2,
        # Boolean - Whether to fill the dataset with a colour
        'datasetFill': False,
    })

    def render(self, header, chart_data):
        self.chart_data = chart_data
        return '''
        <div class="col-md-8">
          <div class="card-head">
            <header>{0}</header>
          </div>
          <div class="card-body height-8">
              <div><canvas id="chart" width="auto" height="auto"></div>
          </div>
        </div>
        '''.format(header)

    def javascript_files(self):
        return [
            'js/libs/d3/d3.v3.js',
            'js/libs/chartjs/Chart.min.js'
        ]

    def css_files(self):
        return []

    def embedded_javascript(self):
        logging.info(self.chart_data)
        logging.info(type(self.chart_data))
        return '''
        console.log("fdsa!");
        var options = {0};
        var data = {1};
        var ctx = document.getElementById("chart").getContext("2d");
        var myLineChart = new Chart(ctx).Line(data, options);
        '''.format(self.chart_options, self.chart_data)
