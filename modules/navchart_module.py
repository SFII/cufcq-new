from modules.linechart_module import LineChartModule
import tornado.web
import logging


class NavChartModule(LineChartModule):

    def render(self, color, raw_data):
        chart_keys = [
            [
                'course_howmuchlearned_average',
                'course_challenge_average',
                'courseoverall_average',
                'course_priorinterest_average'
            ],
            [
                'instructor_effectiveness_average',
                'instructor_respect_average',
                'instructoroverall_average',
                'instructor_availability_average'
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
            ],
            [
                'percent_incomplete',
                'percent_f',
                'percent_d',
                'percent_c',
                'percent_b',
                'average_grade',
                'percent_a',
            ]
        ]
        self.chart_data = []
        self.chart_data.append(self.overtime_linechart_data(raw_data, chart_keys[0]))
        self.chart_data.append(self.overtime_linechart_data(raw_data, chart_keys[1]))
        self.chart_data.append(self.overtime_linechart_data(raw_data, chart_keys[2]))
        self.chart_data.append(self.overtime_linechart_data(raw_data, chart_keys[3]))
        if raw_data['campus'] == 'BD':
            self.chart_data.append(self.overtime_linechart_data(raw_data, chart_keys[4],
                    yearterms_key='grades_yearterms', overtime_key='grades_overtime'))
        else:
            self.chart_data.append([])
        logging.warn(self.chart_data)
        return self.render_string('modules/navchart.html', color=color)

    def embedded_javascript(self):
        logging.info(self.chart_data)
        user_options = tornado.escape.json_encode(self.chart_options())
        line_options = tornado.escape.json_encode(self.chart_options())
        stack_options = tornado.escape.json_encode(self.gradestack_options())
        foo = '''
var user_options={user_options};
var line_options={line_options};
var stack_options={stack_options};
var ctx0 = document.getElementById("chart-0").getContext("2d");
var ctx1 = document.getElementById("chart-1").getContext("2d");
var ctx2 = document.getElementById("chart-2").getContext("2d");
var ctx3 = document.getElementById("chart-3").getContext("2d");
var ctx4 = document.getElementById("chart-4").getContext("2d");
var chart0 = new Chart(ctx0, {{
    type:'line',
    data:{0},
    options:line_options
}});
var chart1, chart2, chart3;
function destroy(chart){{
    if(chart){{
        chart.destroy();
    }}
}};

$('#gnav-0-tab').on('click', function (e) {{
    $(this).tab('show');
    chart0 = new Chart(ctx0, {{
        type:'line',
        data:{0},
        options:line_options
    }});
    destroy(chart1);
    destroy(chart2);
    destroy(chart3);
    destroy(chart4);
}});

$('#gnav-1-tab').on('click', function (e) {{
    $(this).tab('show');
    destroy(chart0);
    chart1 = new Chart(ctx1, {{
        type:'line',
        data:{1},
        options:line_options
    }});
    destroy(chart2);
    destroy(chart3);
    destroy(chart4);
}});

$('#gnav-2-tab').on('click', function (e) {{
    $(this).tab('show');
    destroy(chart0);
    destroy(chart1);
    chart2 = new Chart(ctx2, {{
        type:'line',
        data:{2},
        options:line_options
    }});
    destroy(chart3);
    destroy(chart4);
}});

$('#gnav-3-tab').on('click', function (e) {{
    $(this).tab('show');
    destroy(chart0);
    destroy(chart1);
    destroy(chart2);
    chart3 = new Chart(ctx3, {{
        type:'line',
        data:{3},
        options:line_options
    }});
    destroy(chart4);
}});

$('#gnav-4-tab').on('click', function (e) {{
    $(this).tab('show');
    destroy(chart0);
    destroy(chart1);
    destroy(chart2);
    destroy(chart3);
    chart4 = new Chart(ctx4, {{
        type:'line',
        data:{4},
        options:stack_options
    }});
}});
        '''.format(*self.chart_data, stack_options=stack_options, line_options=line_options, user_options=user_options)
        logging.error(self.chart_data[4])
        logging.warn(foo)
        return foo
