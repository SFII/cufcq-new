from modules.base_module import BaseModule
import tornado.web


class ChartModule(BaseModule):
    chart_data = {}
    chart_id = "chart"

    def chart_options(self):
        return tornado.escape.json_encode({
            'responsive': True,
            'maintainAspectRatio': False,
            'elements': {
                'arc': {},
                'line': {
                    'tension': 0.3,
                    'fill': False
                },
                'point': {},
                'rectangle': {},
            },
            'legend': {
                'display': False,
            },
            'title': {
                'display': False,
            },
            'tooltips': {
                'enabled': True,
                'mode': 'label'
            },
            'scales': {
                'yAxes': [{
                    'ticks': {
                        'beginAtZero': True
                    },
                }]
            }
        })

    def javascript_files(self):
        return [
            'js/libs/chartjs/Chart.min.js'
        ]

    def css_files(self):
        return []

    def render(self):
        return '''
        '''
