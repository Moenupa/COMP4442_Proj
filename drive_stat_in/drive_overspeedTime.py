import os
import sys

from pyspark import SparkContext

i = 's3://comp4442-meng/detail-records/'
o = 's3://comp4442-meng/drive_stat_out/'

sc = SparkContext()

files = sc.wholeTextFiles(i)
records = files.flatMap(lambda file: file[1].split("\n")).map(lambda line: line.split(","))

overspeedTime = records.map(lambda record: (record[0], 0 if (len(record) < 16 or record[15] == "") else int(record[15]))).reduceByKey(lambda a, b: a + b)
overspeedTime.saveAsTextFile(o + "overspeedTime")

sc.stop()