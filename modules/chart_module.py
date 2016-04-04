from modules.base_module import BaseModule
import tornado.web


class ChartModule(BaseModule):
    chart_data = {}
    chart_id = "chart"

    def chart_options(self):
        return {
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
                    'id': "y-axis-1",
                    'ticks': {
                        'beginAtZero': True
                    },
                }]
            }
        }
    def gradestack_options(self):
        options = self.chart_options()
        options['animate'] = False
        options['scales'] = {
            'yAxes': [{
                'id': "y-axis-3",
                'stacked': True,
                'position': 'left',
                'ticks': {
                    'beginAtZero': True,
                    'max': 1.0,
                },
            },
                {
                'id': "y-axis-2",
                'stacked': False,
                'position': 'right',
                'ticks': {
                    'beginAtZero': True,
                    'max': 4.0,
                },
            }]
        }
        return options


    def javascript_files(self):
        return [
            'js/libs/chartjs/Chart.min.js'
        ]

    def css_files(self):
        return []

    def render(self):
        return '''
        '''
