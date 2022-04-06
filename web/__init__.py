from flask import Flask, render_template
import json
from web.db_connector import DBConnector
from werkzeug.exceptions import HTTPException

app = Flask(__name__, static_url_path='/static')

connector = DBConnector()
latest = 0
cur_driver = ''
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
def hello_world():
    return render_template(
        "index.html",
        routes = routes,
        cur = "/about",
        msg = [
            'About page'
        ]
    )

@app.route('/')
def speedmonitor():
    return render_template(
        "index.html",
        routes = routes,
        cur = "/",
        msg = [
            'Welcome to driving Statistics',
            'This platform displays data processed by '
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
    global latest, cur_driver
    cursor = connector.get_db_cursor()

    if cur_driver != driverID:
        latest = 0
        cur_driver = driverID
    
    query = f'select ID, DriverID, CTime, Speed from {connector.SPEED_TABLE} where DriverID = \"{driverID}\" and ID > {latest};'
    cursor.execute(query)
    data = cursor.fetchall()
    
    if len(data) > 0:
        latest = data[-1][0]
    
    # print(query)
    # print('last record:', data[-1])
    return json.dumps([row[2:] for row in data])

@app.route('/api/drivers')
def API_drivers():
    # return json.dumps(['driver%02d' % (i) for i in range(1,11)])
    cursor = connector.get_db_cursor()
    
    query = f'select DriverID from {connector.SUMMARY_TABLE};'
    cursor.execute(query)
    data = cursor.fetchall()
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