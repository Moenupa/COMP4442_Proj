# COMP4442-Proj

## Project Structure

```sh
.
├── backend/                # backend code
├── detail-records/         # records of driving data
├── drive_stat_in/          # source code for processing driving data
├── drive_stat_out/         # output of driving statistics
├── env/                    # local virtualenv, need to set up locally
├── frontend/               # frontend code
│   ├── template/           # html templates
│   ├── main.py             # End-to-end, integration tests (alternatively `e2e`)
│   └── write.py            # Write to the database with real-time data
└── table.sql               # sql to set up the table
```

## Dataset representation

| INDEX | DATASET COLUMN           |
| :---: | :----------------------- |
|   0   | `driverID`               |
|   1   | `carPlateNumber`         |
|   2   | `Latitude`               |
|   3   | `Longtitude`             |
|   4   | `Speed`                  |
|   5   | `Direction`              |
|   6   | `siteName`               |
|   7   | `Time`                   |
|   8   | `isRapidlySpeedup`       |
|   9   | `isRapidlySlowdown`      |
|  10   | `isNeutralSlide`         |
|  11   | `isNeutralSlideFinished` |
|  12   | `neutralSlideTime`       |
|  13   | `isOverspeed`            |
|  14   | `isOverspeedFinished`    |
|  15   | `overspeedTime`          |
|  16   | `isFatigueDriving`       |
|  17   | `isHthrottleStop`        |
|  18   | `isOilLeak`              |

## Database Schema

```sql
DROP TABLE IF EXISTS {summary_table_name};
CREATE TABLE {summary_table_name} (
    DriverID varchar(40) NOT NULL, 
    carPlate varchar(40) NOT NULL, 
    speedUp varchar(40) NOT NULL, 
    slowDown varchar(40) NOT NULL, 
    neutralSlide varchar(40) NOT NULL, 
    neutralSlideTime varchar(40) NOT NULL, 
    overspeed varchar(40) NOT NULL, 
    overspeedTime varchar(40) NOT NULL, 
    fatigue varchar(40) NOT NULL, 
    hthrottleStop varchar(40) NOT NULL, 
    oilLeak varchar(40) NOT NULL, 
    PRIMARY KEY (DriverID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

```sql
DROP TABLE IF EXISTS {speed_table_name};
CREATE TABLE {speed_table_name} (
    ID int(11) unsigned NOT NULL AUTO_INCREMENT, 
    DriverID varchar(40) NOT NULL, 
    Ctime bigint(11) NOT NULL, 
    Speed int(11) NOT NULL, 
    PRIMARY KEY (ID)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT charset=utf8;
```