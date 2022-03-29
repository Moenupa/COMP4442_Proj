from db_connection import DBConnecter

connecter = DBConnecter()
cursor = connecter.create_db_and_get_cursor()
print("Successfully connect to database")

cursor.execute("drop table if exists Summary;")
cursor.execute("CREATE TABLE Summary (DriverID varchar(40) NOT NULL, carPlate varchar(40) NOT NULL, speedUp varchar(40) NOT NULL, slowDown varchar(40) NOT NULL, neutralSlide varchar(40) NOT NULL, neutralSlideTime varchar(40) NOT NULL, overspeed varchar(40) NOT NULL, overspeedTime varchar(40) NOT NULL, fatigue varchar(40) NOT NULL, hthrottleStop varchar(40) NOT NULL, oilLeak varchar(40) NOT NULL, PRIMARY KEY (DriverID)) ENGINE=InnoDB default charset=utf8;")
print("`Summary` table created.")

cursor.execute("drop table if exists Records;")
cursor.execute("CREATE TABLE Records (ID int(11) unsigned not null auto_increment, DriverID varchar(40) not null, Time bigint(11) not null, Speed int(11) not null, PRIMARY KEY (ID)) ENGINE=InnoDB auto_increment=1 default charset=utf8;")
print("`Records` table created.")
