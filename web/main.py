from http.client import TEMPORARY_REDIRECT
from flask import Flask, render_template
import json
import mysql.connector

app = Flask(__name__)

def db_connection():
    # establish db connection
    connection = mysql.connector.connect(
        host = '',
        user = 'admin',
        port = '',
        database = '',
        passwd = '12345678',
        autocommit = True 
    )
    return connection

connection = db_connection()
cursor = connection.cursor()
latest = -1

@app.route('/helloworld')
def hello_world():
    return 'Flask: Hello World'

@app.route('/')
def speedmonitor():
    return render_template("monitor.html")

@app.route('/stat')
def stat():
    return render_template("statistics.html")

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


if __name__ == "__main__":
    app.run(debug=True, port=8888)