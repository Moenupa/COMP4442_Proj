from flask import Flask, render_template, request
import json
import mysql.connector

app = Flask(__name__, static_url_path='/static')

def db_connection():
    # establish db connection
    connection = mysql.connector.connect(
        host='database-1.ca3min6kadhv.us-east-1.rds.amazonaws.com', 
        user='admin', 
        port='3306', 
        passwd='12345678',
        database='Summary',
        autocommit=True
    )
    return connection

latest = -1
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
    }
}

@app.route('/about')
def hello_world():
    return 'Flask: Hello World'

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
    return render_template(
        "index.html",
        routes = routes,
        cur = "/monitor",
        monitor = True
    )

@app.route('/api')
def api():
    connection = db_connection()
    cursor = connection.cursor()
    query = "select id, time, driver, speed from SpeedRecords"
    global latest
    if latest > 0:
        query += " where id > " % (latest)

    cursor.execute(query)
    data = cursor.fetchall()
    
    # update latest data
    latest = data[-1][0] if (len(data) > 0) else latest

    return json.dumps(data)

@app.route('/stat')
def stat():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("use Summary;")
    cursor.execute("select * from SummaryTable;")
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
            'icon': 'mdi-car-side'
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
        "Count of Rapid Speeding Up",
        "Count of Rapid Slow Down",
        "Count of Neutral Slide",
        "Total Time of Neutral Slide",
        "Count of Overspeeding",
        "Total Time of Overspeeding",
        "Count of Fatigue Driving",
        "Count of Hthrottle Stop",
        "Count of Oil Leak",
    ]
    return render_template(
        "index.html", 
        table_data = data, 
        stats = stats, 
        table_headers = table_headers, 
        routes = routes,
        cur = "/stat"
    )

if __name__ == "__main__":
    app.run(debug=True, port=8888)