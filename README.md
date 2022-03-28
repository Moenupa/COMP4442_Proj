# comp4442

## Project Structure

```sh
.
├── detail-records/         # records of driving data
├── drive_stat_in/          # source code for processing driving data
├── drive_stat_out/         # output of driving statistics
├── env/                    # local virtualenv, need to set up locally
├── web/                    # Web Flask application
│   ├── template/           # html templates
│   ├── main.py             # End-to-end, integration tests (alternatively `e2e`)
│   └── write.py            # Write to the database with real-time data
└── table.sql               # sql to set up the table
```

## Dataset representation

```py
dataset = {
    'driverID': 0,
    'carPlateNumber': 1,
    'Latitude': 2,
    'Longtitude': 3,
    'Speed': 4,
    'Direction': 5,
    'siteName': 6,
    'Time': 7,
    'isRapidlySpeedup': 8,
    'isRapidlySlowdown': 9,
    'isNeutralSlide': 10,
    'isNeutralSlideFinished': 11,
    'neutralSlideTime': 12,
    'isOverspeed': 13,
    'isOverspeedFinished': 14,
    'overspeedTime': 15,
    'isFatigueDriving': 16,
    'isHthrottleStop': 17,
    'isOilLeak': 18
}
```