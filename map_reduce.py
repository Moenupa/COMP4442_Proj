'''
@author:        WANG Meng
@time:          March 26, 2022
@description:   MapReduce for COMP4442 on Spark

For a), you are required to display the driving behavior information during the given period in a HTML table. The information includes but not limited to the car plate number, the cumulative number of times of overspeed and fatigue driving, the total time of overspeed and neutral slide.
'''

import os
import sys

from pyspark import SparkContext
from operator import add

d = {
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

# judge whether in 'i'th state
isState = lambda i, arr: len(arr) >= i+1 and len[i] == '1'
init = lambda l: [] if len(sys.argv) != l + 1 else sys.argv[1:]

if __name__ == '__main__':
    io = init(2) # accept 2 args, excluding src.py
    if not io:
        print

    if io:
        (i, o) = io
        sc = SparkContext()
        files = sc.textFile(i)
        line = files.flatMap(lambda text: text[1].split('\n'))
        
        overspeedStat = \
            line.map(
                lambda record: (
                    record[0], 
                    record[d['isOverspeedFinished']] + ',' + record[d['overspeedTime']] \
                    if isState(d['isOverspeedFinished']) else '0,0'
                )
            ).reduceByKey(
                lambda a, b: ','.join(str(i) for i in map(add, eval(a), eval(b)))
                # overspeedCount, overspeedTime element-wise addition
            )
        overspeedStat.collect().saveAsTextFile('StatOS' + o)
        
        fatigueCount = \
            line.map(
                lambda record: (
                    record[0],
                    1 if isState(d['isFatigueDriving']) else 0
                )
            ).reduceByKey(
                add
            )
        fatigueCount.collect().saveAsTextFile('StatFC' + o)
        
        neutralSlideTime = \
            line.map(
                lambda record: (
                    record[0], 
                    eval(record[d['neutralSlideTime']]) if isState(d['isNeutralSlide']) else 0
                )
            ).reduceByKey(
                add
            )
        neutralSlideTime.collect().saveAsTextFile('StatNT' + o)

        sc.stop()
