import os
import sys
from pyspark import SparkContext

(inp, out) = sys.argv[1:]

sc = SparkContext()

text_file = sc.textFile(inp)

counts = text_file.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a + b)
counts.collectAsMap().saveAsTextFile(out + '/counts')

sc.stop()