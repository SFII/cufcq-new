var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var yeartermToDate = function(yearterm){
  year = Math.floor(yearterm / 10);
  sem = yearterm % 10;
  season_string = (sem == 1 ? 'Spring ' : (sem == 4 ? 'Summer ' : 'Fall '));
  month = (sem == 1 ? 0 : (sem == 4 ? 4 : 8));
  return new Date(year, month, 1);
}

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var gradecolor = d3.scale.ordinal().domain(
  ['percent_incomplete','percent_f','percent_d','percent_c','percent_b','percent_a']
).range(
  ['#333333','#d7191c','#fdae61','#ffffbf','#abd9e9','#2c7bb6']
);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")

var area = d3.svg.area()
    .x(function(d) { return x(d.date); })
    .y0(function(d) { return y(d.y0); })
    .y1(function(d) { return y(d.y0 + d.y); });

var stack = d3.layout.stack()
    .values(function(d) { return d.values; });

var svg = d3.select("#grades_overtime_chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

grades_yearterms.forEach(function(d) {
  grades_overtime[d]['grade_data_averages']['date'] = yeartermToDate;
});

var grades = stack(gradecolor.domain().map(function(name) {
  return {
    name: name,
    values: grades_yearterms.map(function(d) {
      return {
        date: yeartermToDate(d),
        y: grades_overtime[d]['grade_data_averages'][name]
      };
    })
  };
}));

x.domain(d3.extent(grades_yearterms, function(d) { return yeartermToDate(d); }));

var grade = svg.selectAll(".grade")
    .areaChartData(grades)
  .enter().append("g")
    .attr("class", "grade");

grade.append("path")
    .attr("class", "area")
    .attr("d", function(d) { return area(d.values); })
    .style("fill", function(d) { return color(d.name); });

grade.append("text")
    .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
    .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.y0 + d.value.y / 2) + ")"; })
    .attr("x", -6)
    .attr("dy", ".35em")
    .text(function(d) { return d.name; });

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);
