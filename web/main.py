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

connection = db_connection()
cursor = connection.cursor()
latest = -1

@app.route('/about')
def hello_world():
    return 'Flask: Hello World'

@app.route('/')
def speedmonitor():
    return render_template("index.html")

@app.route('/monitor')
def monitor():
    return render_template("monitor.html")

@app.route('/api')
def api():
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
    cursor.execute("use Summary;")
    cursor.execute("select * from SummaryTable;")
    data = cursor.fetchall()
    d = {
        # "driver": len(set(eval(i[0]) for i in data)),
        # "cars": len(set(eval(i[1]) for i in data)),
        # "overspeed-count": sum(eval(i[6]) for i in data),
        # "overspeed-time": sum(eval(i[7]) for i in data),
        # "fatigue-count": sum(eval(i[8]) for i in data),
        # "neutralslide-time": sum(eval(i[5]) for i in data),
        "driver": 0,
        "cars": 0,
        "overspeed-count": 0,
        "overspeed-time": 0,
        "fatigue-count": 0,
        "neutralslide-time": 0,
    }
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
    print(data)
    return render_template("stat.html", data = data, stats = d, headers = table_headers)

if __name__ == "__main__":
    app.run(debug=True, port=8888)