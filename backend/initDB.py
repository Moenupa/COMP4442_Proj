from db_connector import DBConnector

connector = DBConnector()
cursor = connector.create_db_and_get_cursor()
print("Successfully connect to database.")

cursor.execute(f"DROP TABLE IF EXISTS {connector.SUMMARY_TABLE};")
cursor.execute(f"CREATE TABLE {connector.SUMMARY_TABLE} (\
        DriverID VARCHAR(40) NOT NULL, \
        carPlate VARCHAR(40) NOT NULL, \
        speedUp VARCHAR(40) NOT NULL, \
        slowDown VARCHAR(40) NOT NULL, \
        neutralSlide VARCHAR(40) NOT NULL, \
        neutralSlideTime VARCHAR(40) NOT NULL, \
        overspeed VARCHAR(40) NOT NULL, \
        overspeedTime VARCHAR(40) NOT NULL, \
        fatigue VARCHAR(40) NOT NULL, \
        hthrottleStop VARCHAR(40) NOT NULL, \
        oilLeak VARCHAR(40) NOT NULL, \
        PRIMARY KEY (DriverID) \
    ) ENGINE=InnoDB DEFAULT charset=utf8;")
print(f"`{connector.SUMMARY_TABLE}` table created.")

cursor.execute(f"DROP TABLE IF EXISTS {connector.SPEED_TABLE};")
cursor.execute(f"CREATE TABLE {connector.SPEED_TABLE} (\
        ID INT(11) UNSIGNED NOT NULL AUTO_INCREMENT, \
        DriverID VARCHAR(40) NOT NULL, \
        CTime BIGINT(11) NOT NULL, \
        Speed INT(11) NOT NULL, \
        IsOverspeed BOOLEAN NOT NULL, \
        PRIMARY KEY (ID) \
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT charset=utf8;")
print(f"`{connector.SPEED_TABLE}` table created.")
