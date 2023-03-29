from highcharts import Highstock
from highcharts.highstock.highstock_helper import jsonp_loader

chart = Highstock()

data_url = 'http://www.highcharts.com/samples/data/jsonp.php?filename=msft-c.json&callback=?'
http://www.highcharts.com/docs/export-module/render-charts-serverside
data = jsonp_loader(data_url, sub_d=None)

options = {
    'title': {
        'text': 'Microsoft Stock Price'
    },
    'xAxis': {
        'type': 'datetime'
    },
    'series': [{
        'name': 'Microsoft Stock Price',
        'data': data,
        'tooltip': {
            'valueDecimals': 2
        }
    }]
}

chart.set_dict_options(options)

exporting_options = {
    'chart': {
        'type': 'image/png',
        'filename': 'my_chart',
        'width': 800,
        'height': 600,
        'backgroundColor': '#FFFFFF'
    }
}

chart.set_dict_options({'exporting': exporting_options})

chart.htmlcontent  # This will display the chart in the Jupyter notebook

# Export the chart as a PNG file
chart.export_chart('my_chart.png')