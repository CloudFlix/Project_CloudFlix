__author__ = 'Srikanth'
import os
from random import shuffle
import train
import test
import operator

"""
#timing a code
import timeit
code = '''
results = {'A': 1, 'B': 2, 'C': 3}
del results['A']
del results['B']
'''
print timeit.timeit(code, number=100000)
"""
#def training_testing(inputlines,type):
# type 1 is splitting the data into training and testing.

fopen = open("./train.csv","r")
datalines = fopen.readlines()
#linenumbers = range(1,len(datalines))  # skipping the first line
datalines = datalines[1:]
#print linenumbers
shuffle(datalines)
percentage = int(0.8*len(datalines))
training_lines = datalines[:percentage]
print "training lines: ",len(training_lines)

#print training_lines
train.train_knn(training_lines,"./test_model_param.p")
print "training complete"

# need to parse the testing_lines to remove the ground truth and repack as list of string.
gold_data = [int(line[0]) for line in datalines[percentage+1:]]
testing_lines =[line[2:] for line in datalines[percentage+1:] ]
print "testing lines: ",len(testing_lines)
test.knn_testing("test_model_param.p",testing_lines,"test_results.txt")

lista = open("test_results.txt","r").readlines()
listb = [int(element.strip().split(",")[1]) for element in lista[1:]]

comparision  = map(operator.sub, gold_data, listb)
print "If score is 0 its perfect return else score is error value"
print "score is", sum([abs(x) for x in comparision])
