import os
import sys

from pyspark import SparkContext

i = 's3://comp4442-meng/detail-records/'
o = 's3://comp4442-meng/drive_stat_out/'

sc = SparkContext()

files = sc.wholeTextFiles(i)
records = files.flatMap(lambda file: file[1].split("\n")).map(lambda line: line.split(","))

speed = records.map(lambda record: (record[0], 0 if (len(record) < 4 or record[3] == "") else eval(record[3])))
speed.collectAsMap().saveAsTextFile(o + "speed")

sc.stop()