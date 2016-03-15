from modules.base_module import BaseModule
import tornado.web


class ChartModule(BaseModule):
    chart_data = {}
    chart_id = "chart"
    chart_options = tornado.escape.json_encode({
        # Whether grid lines are shown across the chart
        'scaleShowGridLines': True,
        # Colour of the grid lines
        'scaleGridLineColor': "rgba(0,0,0,.05)",
        # Width of the grid lines
        'scaleGridLineWidth': 1,
        # Whether to show horizontal lines (except X axis)
        'scaleShowHorizontalLines': True,
        # Whether to show vertical lines (except Y axis)
        'scaleShowVerticalLines': True,
        # Whether the line is curved between points
        'bezierCurve': True,
        # Tension of the bezier curve between points
        'bezierCurveTension': 0.4,
        # Whether to show a dot for each point
        'pointDot': True,
        # Radius of each point dot in pixels
        'pointDotRadius': 2,
        # Pixel width of point dot stroke
        'pointDotStrokeWidth': 1,
        # amount extra to add to the radius to cater for hit detection outside the drawn point
        'pointHitDetectionRadius': 20,
        # Whether to show a stroke for datasets
        'datasetStroke': True,
        # Pixel width of dataset stroke
        'datasetStrokeWidth': 2,
        # Whether to fill the dataset with a colour
        'datasetFill': False,
        # Whether to animate the chart
        'animation': True,
        # Number of animation steps
        'animationSteps': 60,
        # Animation easing effect
        # Possible effects are:
        # [easeInOutQuart, linear, easeOutBounce, easeInBack, easeInOutQuad,
        #  easeOutQuart, easeOutQuad, easeInOutBounce, easeOutSine, easeInOutCubic,
        #  easeInExpo, easeInOutBack, easeInCirc, easeInOutElastic, easeOutBack,
        #  easeInQuad, easeInOutExpo, easeInQuart, easeOutQuint, easeInOutCirc,
        #  easeInSine, easeOutExpo, easeOutCirc, easeOutCubic, easeInQuint,
        #  easeInElastic, easeInOutSine, easeInOutQuint, easeInBounce,
        #  easeOutElastic, easeInCubic]
        'animationEasing': "easeOutQuart",
        # If we should show the scale at all
        'showScale': True,
        # # If we want to override with a hard coded scale
        'scaleOverride': True,
        # # ** Required if scaleOverride is true **
        # # The number of steps in a hard coded scale
        'scaleSteps': 6,
        # # The value jump in the hard coded scale
        'scaleStepWidth': 1,
        # # The scale starting value
        'scaleStartValue': 0,
        # # Colour of the scale line
        # 'scaleLineColor': "rgba(0,0,0,.1)",
        # # Pixel width of the scale line
        # 'scaleLineWidth': 1,
        # # Whether to show labels on the scale
        # 'scaleShowLabels': True,
        # # Interpolated JS string - can access value
        # 'scaleLabel': "",  # "<%=value%>",
        # # Whether the scale should stick to integers, not floats even if drawing space is there
        # 'scaleIntegersOnly': True,
        # # Whether the scale should start at zero, or an order of magnitude down from the lowest value
        # 'scaleBeginAtZero': False,
        # # Scale label font declaration for the scale label
        # 'scaleFontFamily': "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
        # # Scale label font size in pixels
        # 'scaleFontSize': 12,
        # # Scale label font weight style
        # 'scaleFontStyle': "normal",
        # # Scale label font colour
        # 'scaleFontColor': "#666",
        # whether or not the chart should be responsive and resize when the browser does.
        'responsive': True,
        # whether to maintain the starting aspect ratio or not when responsive, if set to False, will take up entire container
        'maintainAspectRatio': False,
        # # Determines whether to draw tooltips on the canvas or not
        # 'showTooltips': True,
        # # Function - Determines whether to execute the customTooltips function instead of drawing the built in tooltips (See [Advanced - External Tooltips](#advanced-usage-custom-tooltips))
        # 'customTooltips': False,
        # # Array - Array of string names to attach tooltip events
        # 'tooltipEvents': ["mousemove", "touchstart", "touchmove"],
        # # Tooltip background colour
        # 'tooltipFillColor': "rgba(0,0,0,0.8)",
        # # Tooltip label font declaration for the scale label
        # 'tooltipFontFamily': "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
        # # Tooltip label font size in pixels
        # 'tooltipFontSize': 14,
        # # Tooltip font weight style
        # 'tooltipFontStyle': "normal",
        # # Tooltip label font colour
        # 'tooltipFontColor': "#fff",
        # # Tooltip title font declaration for the scale label
        # 'tooltipTitleFontFamily': "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
        # # Tooltip title font size in pixels
        # 'tooltipTitleFontSize': 14,
        # # Tooltip title font weight style
        # 'tooltipTitleFontStyle': "bold",
        # # Tooltip title font colour
        # 'tooltipTitleFontColor': "#fff",
        # # pixel width of padding around tooltip text
        # 'tooltipYPadding': 6,
        # # pixel width of padding around tooltip text
        # 'tooltipXPadding': 6,
        # # Size of the caret on the tooltip
        # 'tooltipCaretSize': 8,
        # # Pixel radius of the tooltip border
        # 'tooltipCornerRadius': 6,
        # # Pixel offset from point x to tooltip edge
        # 'tooltipXOffset': 10,
        # # Template string for single tooltips
        # 'tooltipTemplate': "",  # "<%if (label){%><%=label%>: <%}%><%= value %>",
        # # Template string for multiple tooltips
        # 'multiTooltipTemplate': "",  # "<%= value %>",
        # Function - Will fire on animation progression.
        # 'onAnimationProgress': "function(){}",
        # # Function - Will fire on animation completion.
        # 'onAnimationComplete': "function(){}"
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
