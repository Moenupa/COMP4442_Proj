from datetime import datetime
import random
import os
from ast import literal_eval
import time

from db_connector import DBConnector

connector = DBConnector()
cursor = connector.get_db_cursor()

epoch = datetime(1970, 1, 1)
p = '%Y-%m-%d %H:%M:%S'

def writeAllData():
    cursor.execute(f"TRUNCATE TABLE {connector.speed_table_name};")
    print(f'cleared all data in table {connector.speed_table_name}, writing...')
    
    path = './drive_stat_out/speed/'
    for filename in os.listdir(path):
        with open(path + filename) as file:
            for record in file.readlines():
                (driver, time, speed) = literal_eval(record)
                if len(time) == 0:
                    continue
                else:
                    after_epoch = str(int((datetime.strptime(time.replace('\r', ''), p) - epoch).total_seconds() * 1000))
                    query = f"insert into {connector.speed_table_name} (DriverID, Time, Speed) values (\"{0}\",{1},{2})".format(driver, after_epoch, speed)
                    cursor.execute(query)
                    print("inserting ({}, {}, {})\r".format(driver, after_epoch, speed), end='')
    print("writing complete. %40s" % (''))

if __name__ == '__main__':
    writeAllData()