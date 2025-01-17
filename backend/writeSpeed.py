from datetime import datetime
import os
from ast import literal_eval

from db_connector import DBConnector

connector = DBConnector()
cursor = connector.get_db_cursor()

epoch = datetime(1970, 1, 1)
p = '%Y-%m-%d %H:%M:%S'

def writeAllData():
    cursor.execute(f"TRUNCATE TABLE {connector.SPEED_TABLE};")
    print(f'cleared all data in table {connector.SPEED_TABLE}, writing...')
    
    path = './drive_stat_out/speed/'
    for filename in os.listdir(path):
        with open(path + filename) as file:
            for record in file.readlines():
                (driver, time, speed, isOverspeed) = literal_eval(record)
                if len(time) == 0:
                    continue
                else:
                    after_epoch = str(int((datetime.strptime(time.replace('\r', ''), p) - epoch).total_seconds() * 1000))
                    query = f"insert into {connector.SPEED_TABLE} (DriverID, CTime, Speed, IsOverspeed) values (\"{driver}\",{after_epoch},{speed},{isOverspeed});"
                    cursor.execute(query)
                    print(f"inserting ({driver}, {after_epoch}, {speed}, {isOverspeed}) {''*20}\r", end='')
    print("writing complete. %40s" % (''))

if __name__ == '__main__':
    writeAllData()