from ast import literal_eval
import mysql.connector, os

driverdb = mysql.connector.connect(
    host='database-1.ca3min6kadhv.us-east-1.rds.amazonaws.com',
    user='admin', 
    port='3306', 
    passwd='',
    autocommit=True
)
print("Successfully connect to DB")

cursor = driverdb.cursor()
cursor.execute("use Summary;")

path = "./drive_stat_out/"
items = ['carPlate', 'speedUp', 'slowDown', 'neutralSlide', 'neutralSlideTime', 'overspeed', 'overspeedTime', 'fatigue', 'hthrottleStop', 'oilLeak']

for item in items:
    print("Processing: " + item)
    for filename in os.listdir(path + item):
        with open(path + item + "/" + filename) as file:
            for record in file.readlines():
                (k, v) = literal_eval(record)
                if len(k) == 0:
                    continue
                query = "insert into SummaryTable (DriverID, {}) values (\"{}\", \"{}\") on DUPLICATE KEY update {} = VALUES({});".format(item, k, str(v), item, item)
                cursor.execute(query)
                print("\r\tinsert success:", k, v, end="")