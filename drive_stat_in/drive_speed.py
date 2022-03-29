import os
import sys

from pyspark import SparkContext

i = 's3://comp4442-meng/detail-records/'
o = 's3://comp4442-meng/drive_stat_out/'

sc = SparkContext()

files = sc.wholeTextFiles(i)
records = files.flatMap(lambda file: file[1].split("\n")).map(lambda line: line.split(","))

speed = records.map(lambda record: (record[0], record[7], record[4]) if len(record) >= 8 else (record[0], "", ""))
speed.saveAsTextFile(o + "speed")

sc.stop()