import os
import sys

from pyspark import SparkContext

i = 's3://comp4442-meng/detail-records/'
o = 's3://comp4442-meng/drive_stat_out/'

sc = SparkContext()

files = sc.wholeTextFiles(i, use_unicode=False)
records = files.flatMap(lambda file: file[1].decode('utf-8').split("\n")).map(lambda line: line.split(","))

plate = records.map(lambda record: (record[0], '' if len(record) < 2 else record[1])).reduceByKey(lambda a, b: a or b)
plate.saveAsTextFile(o + "plate")

sc.stop()