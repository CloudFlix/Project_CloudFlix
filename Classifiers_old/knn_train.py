__author__ = 'Srikanth'
# KNN
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
from collections import namedtuple
from operator import add
from nltk import stem
from nltk.tokenize import RegexpTokenizer

# splitting the data into training and testing.
'''
TODO: modify feature vector from binary to tf/idf
'''

def train_knn(trainlines,model_fname):
  # worddict [class][filenum][words]
  worddict = defaultdict(lambda: defaultdict(dict))
  gtruth_dict = defaultdict(int)
  idf_dict = defaultdict(float)
  chicount_dict = defaultdict(lambda: defaultdict(int))
  fileindex = 0
  # counting the instances of variable
  class_count = defaultdict(int)
  #chifeat_words = ["_RARE_"]
  chifeat_words = []
  total_docs = len(trainlines)
  uniquewords = set()
  stemmer = stem.PorterStemmer()
  stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 'can', 'will', 'just', 'should', 'now','movie','would','thing','film','cinema','movie','movies','cinemas','tv','documentary','y']
  '''
  stopwords.extend(string.punctuation)
  stopwords = set(stopwords)
  '''
  tokenizer = RegexpTokenizer(r'\w+')
  exp_allnums = re.compile('^[-./]*[0-9][-0-9.,:/]+$')
  exp_wordnums = re.compile('^[A-Za-z]+[0-9]+[-/0-9.A-Za-z]*$')
  exp_numwords = re.compile('^[0-9]?[0-9]+[-./A-Za-z]+$')

  for line in trainlines:
    line = line.strip().lower()
    fileindex = fileindex+1
    gtruth_dict[fileindex]= int(line[0])
    class_count[int(line[0])] += 1
    #tokenlist = word_tokenize(commentwords)
    commentline = line[3:-1]
    commentline = commentline.replace("it's","it is")
    commentline = commentline.replace("won't","will not")
    commentline = commentline.replace("can't","cannot")
    commentline = commentline.replace("n't"," not")
    commentline = commentline.replace("'ll"," will")
    commentwords = tokenizer.tokenize(commentline)
    # Numeric words
    allnumkeys = set([m.group(0) for word in commentwords for m in [exp_allnums.search(word)] if m ])
    # identify exclusive alphanumeric
    wordnumset = set([m.group(0) for word in commentwords for m in [exp_wordnums.search(word)] if m ])
    # identify exclusive numericalpha
    numwordset = set([m.group(0) for word in commentwords for m in [exp_numwords.search(word)] if m ])
    # removing the punctuations and stop words

    commentwords = [stemmer.stem(x) for x in commentwords if stemmer.stem(x) not in set(stopwords) | allnumkeys| set(wordnumset)| set(numwordset)]

    wordset = set(commentwords)
    # for single occurance of word increment
    for word in wordset:
      idf_dict[word] += 1
    uniquewords.update(wordset)
    worddict[fileindex] = commentwords

    # getting the chisquare_dict
    for word in commentwords:
      chicount_dict[word][int(line[0])] += 1
  # Setting IDF for each doc.
  for key,value in idf_dict.iteritems():
    idf_dict[key] = float(total_docs)/value

  # calculating chi-square value for each word.
  for word in uniquewords:
    # subscript (term, class)
    n11 = chicount_dict[word][1]+1
    n10 = chicount_dict[word][0]+1
    n01 = class_count[1] -n11
    n00 = class_count[0] -n10
    num = (n11 + n10 + n01 + n00)* ( n11*n00 - n10*n01)*(n11*n00 - n10*n01)
    den = (n11 + n01)*(n11 + n10)*(n10 + n00)*(n01 + n00)
    chivalue = float(num)/den
    if chivalue >0 :# other values are
      # 10.83 -- 0.001
      # 7.88  -- 0.005
      # 6.63  -- 0.01
      # 3.84  -- 0.05
      # 2.71  -- 0.1
      chifeat_words.append(word)
  #print chifeat_words
  print len(chifeat_words),"\n"

  uniquewords  = chifeat_words
  # enumeration of unique words as enumeration is not existing in python
  feat_len = len(uniquewords)
  uniquewords = list(uniquewords)
  enumwords_dict = defaultdict(int)
  iter = 0
  for word in uniquewords:
    enumwords_dict[word] = iter
    iter += 1
  #initialising centroid matrix
  centroid_mat = defaultdict(list)
  centroid_mat[0] = [0]*feat_len
  centroid_mat[1] = [0]*feat_len

  for findex in range(1,len(trainlines)+1):
    featvect = [0]*feat_len
    words = worddict[findex]
    for word in words:
      if word in uniquewords:
      #featvect[enumwords_dict[word]] += idf_dict[word]/len(words) # normalising length of sentence.
        featvect[enumwords_dict[word]] += float(1)#/len(words) # normalising length of sentence.
      else:
        featvect[enumwords_dict["_RARE_"]] += float(1)#/len(words) # normalising length of sentence.
      # replace this value 1 with frequency or tf/idf for better results.
    centroid_mat[gtruth_dict[findex]] = map(add,centroid_mat[gtruth_dict[findex]],featvect)
  for cl in [0,1]:
    centroid_mat[cl] = map(lambda x: x/class_count[cl], centroid_mat[cl])
  fopen = open(model_fname,"wb")
  pickle.dump([centroid_mat,enumwords_dict,idf_dict],fopen)

  fopen.close()

# main method
def main(karg):
  if len(karg) !=3:
    print "Usage error: Use python train.py train.csv model_file"
    sys.exit(0)
  fopen = open(karg[1])
  trainlines = fopen.readlines()
  train_knn(trainlines[1:],karg[2])

main(sys.argv)