import os
import sys

from pyspark import SparkContext

i = 's3://comp4442-meng/detail-records/'
o = 's3://comp4442-meng/drive_stat_out/'

sc = SparkContext()

files = sc.wholeTextFiles(i)
records = files.flatMap(lambda file: file[1].split("\n")).map(lambda line: line.split(","))

overspeedCount = records.map(lambda record: (record[0], 0 if (len(record) < 15 or record[14] == "") else 1)).reduceByKey(lambda a, b: a + b)
overspeedCount.saveAsTextFile(o + "overspeedCount")

sc.stop()