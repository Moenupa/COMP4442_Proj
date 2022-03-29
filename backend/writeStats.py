from ast import literal_eval
import os

from db_connection import DBConnecter

connecter = DBConnecter()
cursor = connecter.db_cursor()
print("Successfully connect to DB")

path = "./drive_stat_out/"
items = ['carPlate', 'speedUp', 'slowDown', 'neutralSlide', 'neutralSlideTime', 'overspeed', 'overspeedTime', 'fatigue', 'hthrottleStop', 'oilLeak']

for item in items:
    print("Processing: %-20s" % (item))
    for filename in os.listdir(path + item):
        with open(path + item + "/" + filename) as file:
            for record in file.readlines():
                (k, v) = literal_eval(record)
                if len(k) == 0:
                    continue
                query = "insert into Summary (DriverID, {}) values (\"{}\", \"{}\") on DUPLICATE KEY update {} = VALUES({});".format(item, k, str(v), item, item)
                cursor.execute(query)
                print("insert success:", k, v, "\r", end="")
                
print("writeStats Completed!")