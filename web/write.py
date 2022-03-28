import time
import mysql.connector
import random

def db_connection():
    # establish db connection
    connection = mysql.connector.connect(
        host='',
        user='admin',
        port='',
        database = ''
        passwd = '12345678',
        autocommit = True
    )
    return connection

db = db_connection()
cursor = db.cursor()

def getData():
    speed = random.randint(1,10)
    t = int(time.time())
    driver = 'driver'
    
    # return a dict
    return {
        'time': t,
        'driver': driver,
        'speed': speed
    }

def execute():
    # get data
    data = getData()
    
    # mysql query to insert data to db
    sql = "insert into SpeedRecords (time, driver, speed) values ({0},{1},{2})".format(data['time'], data['driver'], data['speed'])
    ret = cursor.execute(sql)