
js_location = "https://www.google.com/jsapi"


def ClassicBar(title, yaxis, xaxis, yrows, xrows, width, height):
    global js_location
    html = '<html>\n<head>'
    html += '\n<script type="text/javascript" src="' + str(js_location) + '"></script>\n<script type="text/javascript">'
    html += "\n   google.load('visualization', '1.0', {'packages':['corechart']});\n      google.setOnLoadCallback(drawChart);\n     function drawChart() {\n        var data = new google.visualization.DataTable();\n"
    html += "       data.addColumn('string', '" + str(yaxis) + "');\n"
    html += "       data.addColumn('number', '" + str(xaxis) + "');\n"
    html += "       data.addRows([\n"
    x = 0
    for yrow in yrows:
            html += "         ['" + str(yrow) + "', " + str(xrows[x]) + "],\n"
            x += 1
    html += "       ]);\n"
    html += "       var options = {'title':'" + str(title) + "',\n           'width':"
    html += str(width) + ",\n           'height':" + str(height) + ", 'chartArea': {'height': '96%'}, 'legend': {'position': 'bottom'} \n};\n\n"
    html += "        var chart = new google.visualization.BarChart(document.getElementById('chart_div'));\n    chart.draw(data, options);  }"
    html += "\n    </script>\n   </head>\n  <body>"
    html += '<center><div id="chart_div" style="width: ' + str(width) + 'px; height: ' + str(height) + 'px;"></div></center></body></html>'
    return html


