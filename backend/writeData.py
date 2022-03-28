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
path = "../drive_stat_out/"
items = ['carPlate', 'speedUp', 'slowDown', 'neutralSlide', 'neutralSlideTime', 'overspeed', 'overspeedTime', 'fatigue', 'hthrottleStop', 'oilLeak']
for item in items:
    print("processing: " + item)
    files = os.listdir(path + item)
    for file in files:
        with open(path + item + "/" + file) as outputFile:
            records = outputFile.read()
            if records != '':
                for record in records.split("\n"):
                    if record != '':
                        (key, value) = literal_eval(record)
                        if key != '':
                            sql = "insert into SummaryTable (DriverID, {}) values (\"{}\", \"{}\") on DUPLICATE KEY update {} = VALUES({});".format(item, key, str(value), item, item)
                            cursor.execute(sql)
                            print(key, value)