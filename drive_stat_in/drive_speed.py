import os
import sys

from pyspark import SparkContext

i = 's3://comp4442-meng/detail-records/'
o = 's3://comp4442-meng/drive_stat_out/'

sc = SparkContext()

files = sc.wholeTextFiles(i)
records = files.flatMap(lambda file: file[1].split("\n")).map(lambda line: line.split(","))

isOverspeed = 0
def func(record):
    global isOverspeed
    if len(record) >= 14 and record[13] == "1":
        isOverspeed = 1
    elif len(record) >= 15 and record[14] == "1":
        isOverspeed = 0
    if len(record) >= 8:
        return (record[0], record[7], record[4], isOverspeed)
    else:
        return (record[0], "", "", isOverspeed)
speed = records.map(func)
speed.saveAsTextFile(o + "speed")

sc.stop()