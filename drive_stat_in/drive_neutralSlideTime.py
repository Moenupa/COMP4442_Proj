import os
import sys

from pyspark import SparkContext

i = 's3://comp4442-meng/detail-records/'
o = 's3://comp4442-meng/drive_stat_out/'

sc = SparkContext()

files = sc.wholeTextFiles(i)
records = files.flatMap(lambda file: file[1].split("\n")).map(lambda line: line.split(","))

neutralSlideTime = records.map(lambda record: (record[0], 0 if (len(record) < 13 or record[12] == "") else int(record[12]))).reduceByKey(lambda a, b: a + b)
neutralSlideTime.saveAsTextFile(o + "neutralSlideTime")

sc.stop()