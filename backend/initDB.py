import mysql.connector, os

driverdb = mysql.connector.connect(
    host='database-1.ca3min6kadhv.us-east-1.rds.amazonaws.com', 
    user='admin', 
    port='3306', 
    passwd='12345678', 
    autocommit=True
)
print("Successfully connect to DB")

cursor = driverdb.cursor()
cursor.execute("drop database if exists Summary;")
cursor.execute("create database `Summary` CHARACTER SET utf8 COLLATE utf8_general_ci;")
cursor.execute("use Summary;")
cursor.execute("drop table if exists SummaryTable;")
cursor.execute("CREATE TABLE IF NOT EXISTS SummaryTable (DriverID varchar(40) NOT NULL, carPlate varchar(40) NOT NULL, speedUp varchar(40) NOT NULL, slowDown varchar(40) NOT NULL, neutralSlide varchar(40) NOT NULL, neutralSlideTime varchar(40) NOT NULL, overspeed varchar(40) NOT NULL, overspeedTime varchar(40) NOT NULL, fatigue varchar(40) NOT NULL, hthrottleStop varchar(40) NOT NULL, oilLeak varchar(40) NOT NULL, PRIMARY KEY (DriverID)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
cursor.execute("describe SummaryTable;")