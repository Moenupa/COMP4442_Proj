from db_connector import DBConnector

connector = DBConnector()
cursor = connector.create_db_and_get_cursor()
print("Successfully connect to database.")

cursor.execute(f"DROP TABLE IF EXISTS {connector.summary_table_name};")
cursor.execute(f"CREATE TABLE {connector.summary_table_name} (DriverID varchar(40) NOT NULL, carPlate varchar(40) NOT NULL, speedUp varchar(40) NOT NULL, slowDown varchar(40) NOT NULL, neutralSlide varchar(40) NOT NULL, neutralSlideTime varchar(40) NOT NULL, overspeed varchar(40) NOT NULL, overspeedTime varchar(40) NOT NULL, fatigue varchar(40) NOT NULL, hthrottleStop varchar(40) NOT NULL, oilLeak varchar(40) NOT NULL, PRIMARY KEY (DriverID)) ENGINE=InnoDB DEFAULT charset=utf8;")
print(f"`{connector.summary_table_name}` table created.")

cursor.execute(f"DROP TABLE IF EXISTS {connector.speed_table_name};")
cursor.execute(f"CREATE TABLE {connector.speed_table_name} (ID int(11) unsigned NOT NULL AUTO_INCREMENT, DriverID varchar(40) NOT NULL, Time bigint(11) NOT NULL, Speed int(11) NOT NULL, PRIMARY KEY (ID)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT charset=utf8;")
print(f"`{connector.speed_table_name}` table created.")
