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

## Deployment

1. Create a new mysql database on AWS. Make sure to assign it to a correct security group. Otherwise you may not even establish connection with the database.
2. Modify `.env` file to update the following keys:
    ```ini
    HOST="<database url>"
    ADMIN="<user, default is admin>"
    PORT="<port, default is 3306>"
    PASSWD="<password>"
    ```
3. Setup and start a virtual environment
    ```sh
    cd ../COMP4442_Proj             # change dir to the project directory
    pip install virtualenv          # install a virtual environment
    virtualenv env                  # initialize a virtual environment into env
    source env/bin/activate         # start a virtual environment session
    ```
4. Install python dependencies in virtual environment
    ```sh
    pip install -r requirements.txt
    ```
5. Initialize database schema  
    ```sh
    python ./backend/initDB.py
    ```
    If you do not see `Successfully connect to database message`, recheck step1 and step2.  
6. Write into database
    ```sh
    python ./backend/writeStats.py
    python ./backend/writeSpeed.py  # this may take ages
    ```
    Note that executing `python ./backend/writeSpeed.py` may take a very long time.  
    Yon can consider execute it after step 7 or leave it alone.
7. Start a new terminal session and start flask
    ```sh
    python ./frontend/main.py
    ```
8. Hit the link in step7's prompt or simply visit [http://localhost:8888/](http://localhost:8888/)

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