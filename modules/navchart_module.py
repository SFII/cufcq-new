from modules.linechart_module import LineChartModule
import tornado.web
import logging


class NavChartModule(LineChartModule):

    def render(self, color, raw_data):
        chart_keys = [
            [
                'instructor_effectiveness_average',
                'instructor_respect_average',
                'instructoroverall_average',
                'instructor_availability_average'
            ],
            [
                'course_howmuchlearned_average',
                'course_challenge_average',
                'courseoverall_average',
                'course_priorinterest_average'
            ],
            [
                'TTT_instructoroverall_average',
                'OTH_instructoroverall_average',
                'TA_instructoroverall_average'
            ],
            [
                'GR_courseoverall_average',
                'UD_courseoverall_average',
                'LD_courseoverall_average'
            ]
        ]
        self.chart_data = [self.overtime_linechart_data(raw_data, key) for key in chart_keys]
        logging.warn(self.chart_data)
        return self.render_string('modules/navchart.html', color=color)

    def embedded_javascript(self):
        logging.info(self.chart_data)
        options = self.chart_options()
        foo = '''
var options={options};
var ctx0 = document.getElementById("chart-0").getContext("2d");
var ctx1 = document.getElementById("chart-1").getContext("2d");
var ctx2 = document.getElementById("chart-2").getContext("2d");
var ctx3 = document.getElementById("chart-3").getContext("2d");
var chart0 = new Chart(ctx0, {{
    type:'line',
    data:{0},
    options:options
}});
var chart1, chart2, chart3;

$('#gnav-0-tab').on('click', function (e) {{
    $(this).tab('show');
    chart0 = new Chart(ctx0, {{
        type:'line',
        data:{0},
        options:options
    }});
    chart1.destroy();
    chart2.destroy();
    chart3.destroy();
}});

$('#gnav-1-tab').on('click', function (e) {{
    $(this).tab('show');
    chart0.destroy();
    chart1 = new Chart(ctx1, {{
        type:'line',
        data:{1},
        options:options
    }});
    chart2.destroy();
    chart3.destroy();
}});

$('#gnav-2-tab').on('click', function (e) {{
    $(this).tab('show');
    chart0.destroy();
    chart1.destroy();
    chart2 = new Chart(ctx2, {{
        type:'line',
        data:{2},
        options:options
    }});
    chart3.destroy();
}});

$('#gnav-3-tab').on('click', function (e) {{
    $(this).tab('show');
    chart0.destroy();
    chart1.destroy();
    chart2.destroy();
    chart3 = new Chart(ctx3, {{
        type:'line',
        data:{3},
        options:options
    }});
}});
        '''.format(*self.chart_data, options=options)
        logging.warn(foo)
        return foo
