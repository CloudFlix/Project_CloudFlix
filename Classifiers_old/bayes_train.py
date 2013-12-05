__author__ = 'Srikanth'
# TODO CHI-square.
# Naive Bayes
import os
import shlex
from collections import defaultdict
import string
import re
from random import shuffle
from collections import Counter
import math
import sys
import cPickle as pickle
from nltk import stem
from nltk.tokenize import RegexpTokenizer
from nltk import word_tokenize

# lambda function to create nested dictionary
def lambdafn_float():
  return defaultdict(float)
# splitting the data into training and testing.
def preprocess(trainlines):
  worddict = defaultdict(lambda: defaultdict(int))
  chisquare_dict =  defaultdict(float)

  chicount_dict = defaultdict(lambda: defaultdict(int))
  gtruth_dict = defaultdict(int)
  idf_dict = defaultdict(float)
  index = 0
  stemmer = stem.PorterStemmer()
  total_docs = len(trainlines)
  stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 'can', 'will', 'just', 'should', 'now','movie','would','thing','film','cinema','movie','movies','cinemas','tv','documentary','y']
  stopwords = set(stopwords)
  tokenizer = RegexpTokenizer(r'\w+')

  # Regular Expressions to remove alpha numerics
  exp_allnums = re.compile('^[-./]*[0-9][-0-9.,:/]+$')
  exp_wordnums = re.compile('^[A-Za-z]+[0-9]+[-/0-9.A-Za-z]*$')
  exp_numwords = re.compile('^[0-9]?[0-9]+[-./A-Za-z]+$')

  for line in trainlines:
    line = line.strip().lower()
    index = index+1
    gtruth_dict[index]= int(line[0])

    #tokenlist = word_tokenize(commentwords)
    commentline = line[3:-1]
    commentline = commentline.replace("it's","it is")
    commentline = commentline.replace("won't","will not")
    commentline = commentline.replace("can't","cannot")
    commentline = commentline.replace("n't"," not")
    commentline = commentline.replace("'ll"," will")
    commentwords = tokenizer.tokenize(commentline)
    commentwords = [stemmer.stem(x) for x in commentwords if stemmer.stem(x) not in stopwords]

    wordset = list(set(commentwords))
    # counting freq of docs with the "word"
    for word in wordset:
      idf_dict[word] += 1
    # adding to dictionary
    for word in commentwords:
      worddict[int(line[0])][word]+= 1
      chicount_dict[word][int(line[0])] += 1

  # removing numerics as key words
  allnumkeys = [m.group(0) for word in set(worddict[0].iterkeys())|set(worddict[1].iterkeys()) for m in [exp_allnums.search(word)] if m ]
  # identify exclusive alphanumeric
  wordnumset = [m.group(0) for word in set(worddict[0].iterkeys())|set(worddict[1].iterkeys()) for m in [exp_wordnums.search(word)] if m ]
  # identify exclusive numericalpha
  numwordset = [m.group(0) for word in set(worddict[0].iterkeys())|set(worddict[1].iterkeys()) for m in [exp_numwords.search(word)] if m ]

  # removing all numerics and alpha numerics.
  allremovablekeys =allnumkeys+numwordset+wordnumset
  for numstr in allremovablekeys:
    worddict[1].pop(numstr,None)
    worddict[0].pop(numstr,None)
    chicount_dict[1].pop(numstr,None)
    chicount_dict[0].pop(numstr,None)
    idf_dict.pop(numstr,None)

  # Setting IDF now
  for key,value in idf_dict.iteritems():
    idf_dict[key] = float(total_docs)/value

  return [worddict, gtruth_dict, idf_dict, chicount_dict]

# multinomial method
def multinomial_training(worddict, gtruth_dict, idf_dict,chicount_dict, readlines, model_param):
  class_count = Counter(gtruth_dict.values())
  cond_prob = defaultdict(lambdafn_float)

  prior_dict = defaultdict(float)
  denomdict = defaultdict(float)
  uniquewords = set(worddict[0].keys()+worddict[1].keys())
  # calculating chi-square value for each word.
  chiremoved_words = []
  for word in uniquewords:
    # subscript (term, class)
    n11 = chicount_dict[word][1]+1
    n10 = chicount_dict[word][0]+1
    n01 = class_count[1] -n11
    n00 = class_count[0] -n10
    num = (n11 + n10 + n01 + n00)* ( n11*n00 - n10*n01)*(n11*n00 - n10*n01)
    den = (n11 + n01)*(n11 + n10)*(n10 + n00)*(n01 + n00)
    chivalue = float(num)/den
    if chivalue < 0:
      # 10.83 -- 0.001
      # 7.88  -- 0.005
      # 6.63  -- 0.01
      # 3.84  -- 0.05
      # 2.71  -- 0.1
      worddict[1].pop(word,None)
      worddict[0].pop(word,None)
      chiremoved_words.append(word)
  print "length of chiwords:",len(set(uniquewords)-set(chiremoved_words)) ,"\n"
  #print "chiwords:\n",set(uniquewords)-set(chiremoved_words)

  for cl in [0,1]:
    sum_ = sum(worddict[cl].itervalues())
    #print "sum",sum_,"len", len(worddict[cl])
    denomdict[cl] = len(worddict[cl])+ sum_
    #denomdict[cl] = sum_
    prior_dict[cl] = float(class_count[cl])/len(readlines)
    for word in worddict[cl]:
      cond_prob[cl][word] = float(worddict[cl][word]+1)/denomdict[cl]
      #cond_prob[cl][word] = float(worddict[cl][word])/denomdict[cl]
      # TODO remove 1? removed now

    '''
    for word in worddict[cl]:
      # Doing the idf* tf term
      #cond_prob[cl][word] = idf_dict[word] * float(worddict[cl][word]+1)/sum_  # replacing tf with tf* idf value here.
      cond_prob[cl][word] = float(worddict[cl][word]+1)/sum_  # replacing tf with tf* idf value here.
    '''
  fopen = open(model_param,"wb")
  pickle.dump([prior_dict, cond_prob,idf_dict,denomdict],fopen)
  fopen.close()
  #return [worddict, prior_dict, cond_prob]

def main(karg):
  if len(karg) != 3:
    print "Usage error: Use python train.py training.csv model_file"
    sys.exit(0)
  fopen = open(karg[1])
  trainlines = fopen.readlines()
  [worddict,gtruth_dict,idf_dict,chicount_dict] = preprocess(trainlines[1:])
  multinomial_training(worddict,gtruth_dict,idf_dict,chicount_dict,trainlines[1:],karg[2])
  print "training done"

main(sys.argv)