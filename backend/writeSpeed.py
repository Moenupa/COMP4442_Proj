from datetime import datetime
import random
import os
from ast import literal_eval
import time

from db_connection import DBConnecter

connecter = DBConnecter()
cursor = connecter.db_cursor()

epoch = datetime(1970, 1, 1)
p = '%Y-%m-%d %H:%M:%S'

def writeAllData():
    cursor.execute("TRUNCATE TABLE Records;")
    print('clearing all table records')
    
    print('writing all speed data into `Records` table')
    path = './drive_stat_out/speed/'
    for filename in os.listdir(path):
        with open(path + filename) as file:
            for record in file.readlines():
                (driver, time, speed) = literal_eval(record)
                if len(time) == 0:
                    continue
                else:
                    after_epoch = str(int((datetime.strptime(time.replace('\r', ''), p) - epoch).total_seconds() * 1000))
                    query = "insert into Records (DriverID, Time, Speed) values (\"{0}\",{1},{2})".format(driver, after_epoch, speed)
                    cursor.execute(query)
                    print("inserting ({}, {}, {})\r".format(driver, after_epoch, speed), end='')
    print("writing complete. %40s" % (''))

def getData():
    global lastest
    query = "select * from Records where time > lastest"
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
    sql = "insert into Records (time, driver, speed) values ({0},{1},{2})".format(data['time'], data['driver'], data['speed'])
    ret = cursor.execute(sql)

if __name__ == '__main__':
    writeAllData()