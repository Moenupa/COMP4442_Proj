from flask import Flask, render_template, request
import json

from web.db_connector import DBConnector
from werkzeug.exceptions import HTTPException

app = Flask(__name__, static_url_path='/static')

connector = DBConnector()
latest = 0
routes = {
    '/': {
        'title': 'Welcome',
        'icon': 'mdi-home'
    },
    '/stat': {
        'title': 'Statistics',
        'icon': 'mdi-table'
    },
    '/monitor': {
        'title': 'Monitor',
        'icon': 'mdi-chart-areaspline'
    },
    '/about': {
        'title': 'About',
        'icon': 'mdi-information'
    },
}

@app.route('/about')
def about():
    return render_template(
        "index.html",
        routes = routes,
        cur = "/about",
        msg = [
            "The page is developed by the group \"JustForCredit\" using Python and HTML. The website is deployed using Amazon Web Services (AWS). The real-time data is visualized on the web page using Flask. "
        ]
    )

@app.route('/')
def welcome():
    return render_template(
        "index.html",
        routes = routes,
        cur = "/",
        msg = [
           "Welcome to Driving Statistics!",
           "",
           "This platform provides real-time driving behavior analysis which helps to identify dangerous driving behaviors to avoid traffic accidents.",
            "The \"Statistics\" page shows a summary of the driving behavior of 10 drivers between 1st and 11th January 2017. ",
            "The \"Monitor\" page monitors the driving speed of each driver in real time. It will issue a warning to driver when the driver is speeding. Users can select a driver from the dropdown menu at the top. The diagram will update every 30 seconds. ",
            "",
            "This platform displays data processed by Spark. "
        ]
    )

@app.route('/monitor')
def monitor():
    drivers = json.loads(API_drivers())

    return render_template(
        "index.html",
        routes = routes,
        cur = "/monitor",
        drivers = drivers,
        monitor = True
    )

@app.route('/api/speed/<driverID>')
def API_speed(driverID):
    global latest
    cursor = connector.get_db_cursor()
    
    refresh = request.args.get('refresh', default = 0, type = int)
    if refresh == 1:
        latest = 0
    
    query = f'select * from {connector.SPEED_TABLE} where DriverID = \"{driverID}\" and ID > {latest};'
    cursor.execute(query)
    data = cursor.fetchall()
    
    if len(data) > 0:
        latest = data[-1][0]
    
    # print(query)
    # print('last record:', data[-1])
    connector.close_connection()
    return json.dumps([row[2:4] for row in data])

@app.route('/api/isOverspeed/<driverID>')
def API_overspeed(driverID):
    cursor = connector.get_db_cursor()
    query = f'select * from {connector.SPEED_TABLE} where DriverID = \"{driverID}\" ORDER BY ID DESC LIMIT 1;'
    cursor.execute(query)
    data = cursor.fetchall()
    connector.close_connection()
    print(data[0][-1])
    return json.dumps(data[0][-1])

@app.route('/api/drivers')
def API_drivers():
    # return json.dumps(['driver%02d' % (i) for i in range(1,11)])
    cursor = connector.get_db_cursor()
    
    query = f'select DriverID from {connector.SUMMARY_TABLE};'
    cursor.execute(query)
    data = cursor.fetchall()
    connector.close_connection()
    return json.dumps([id for row in data for id in row])

@app.route('/stat')
def stat():
    cursor = connector.get_db_cursor()
    cursor.execute(f'select * from {connector.SUMMARY_TABLE};')
    data = cursor.fetchall()
    stats = [
        {
            'title': 'total drivers',
            'color': 'green',
            'num': len(set(i[0] for i in data)),
            'append': '',
            'icon': 'mdi-account'
        },
        {
            'title': 'total vehicles',
            'color': 'blue',
            'num': len(set(i[1] for i in data)),
            'append': '',
            'icon': 'mdi-car'
        },
        {
            'title': 'total neutralslide time',
            'color': 'indigo',
            'num': sum(eval(i[5]) for i in data),
            'append': 'seconds',
            'icon': 'mdi-road'
        },
        {
            'title': 'overspeed count',
            'color': 'pink',
            'num': sum(eval(i[6]) for i in data),
            'append': 'times',
            'icon': 'mdi-speedometer'
        },
        {
            'title': 'total overspeed time',
            'color': 'red',
            'num': sum(eval(i[7]) for i in data),
            'append': 'seconds',
            'icon': 'mdi-timelapse'
        },
        {
            'title': 'fatigue count',
            'color': 'orange',
            'num': sum(eval(i[8]) for i in data),
            'append': 'times',
            'icon': 'mdi-sleep'
        },
    ]
    table_headers = [
        "DriverID",
        "Car Plate",
        "Rapid Speed-Ups",
        "Rapid Slow-Downs",
        "Neutral Slides",
        "Neutral Slide Time",
        "Over-speed Count",
        "Over-speed Time",
        "Fatigue-Drivings",
        "Hthrottle Stops",
        "Oil Leaks",
    ]
    return render_template(
        "index.html", 
        table_data = data, 
        stats = stats, 
        table_headers = table_headers, 
        routes = routes,
        cur = "/stat"
    )

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template("error.html", code = e.code, title = f'{e.code} {e.name.upper()}')

if __name__ == "__main__":
    app.run(debug=True)