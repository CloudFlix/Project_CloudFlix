__author__ = 'Srikanth'
#  KNN
import os,sys
import shlex
from collections import defaultdict
import string
import re
from random import shuffle
from collections import Counter
import math,cPickle as pickle
from nltk import stem
from nltk.tokenize import RegexpTokenizer

def knn_testing(modelfile,testlines,predictionfile):
  linecount = 0
  [centroid_mat,enumwords_dict,idf_dict] = pickle.load( open( modelfile, "rb" ) )
  stemmer = stem.PorterStemmer()
  stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 'can', 'will', 'just', 'should', 'now','movie','would','thing','film','cinema','movie','movies','cinemas','tv','documentary','y']
  '''
  stopwords.extend(string.punctuation)
  stopwords = set(stopwords)
  '''
  exp_allnums = re.compile('^[-./]*[0-9][-0-9.,:/]+$')
  exp_wordnums = re.compile('^[A-Za-z]+[0-9]+[-/0-9.A-Za-z]*$')
  exp_numwords = re.compile('^[0-9]?[0-9]+[-./A-Za-z]+$')
  tokenizer = RegexpTokenizer(r'\w+')
  scorefile = open(predictionfile,"w")

  scorefile.write("Id,Category\n")
  print "length of vector: ", len(enumwords_dict)
  for line in testlines:
    linecount += 1
    line = line.strip().lower()
    line = line.replace("it's","it is")
    line = line.replace("won't","will not")
    line = line.replace("can't","cannot")
    line = line.replace("'ll"," will")
    line = line.replace("n't"," not")
    commentwords = tokenizer.tokenize(line)

    allnumkeys = set([m.group(0) for word in commentwords for m in [exp_allnums.search(word)] if m ])
    # identify exclusive alphanumeric
    wordnumset = set([m.group(0) for word in commentwords for m in [exp_wordnums.search(word)] if m ])
    # identify exclusive numericalpha
    numwordset = set([m.group(0) for word in commentwords for m in [exp_numwords.search(word)] if m ])
    commentwords = [stemmer.stem(x) for x in commentwords if stemmer.stem(x) not in set(stopwords) | allnumkeys| set(wordnumset)| set(numwordset)]

    linevec = [float(0)]*len(enumwords_dict)
    '''
    for word in commentwords:
      if word in idf_dict:
        linevec[enumwords_dict[word]] += idf_dict[word]/len(commentwords) # this is eq to tf*idf
      else:
        linevec[enumwords_dict[word]] += 1/len(commentwords) # eq to tf
    '''
    for word in commentwords:
      if word in enumwords_dict:
        linevec[enumwords_dict[word]] += float(1)

      else: # NO RARE submission
        linevec[enumwords_dict["_RARE_"]] += float(1) # eq to tf

    scorelist = []

    for cl in [0,1]:
      centvec = centroid_mat[cl]
      dist = math.sqrt(sum( (a - b)**2 for a, b in zip(centvec,linevec)))
      scorelist.append(dist)

    score = scorelist.index(min(scorelist))
    scorefile.write(str(linecount)+","+str(score)+"\n")
  scorefile.close()

def main(karg):
  # Script main file.
  if len(sys.argv) !=4:
    print"Usage error: Use python test.py model_file test_file.csv prediction_file"
    sys.exit(0)

  fopen = open(karg[2])
  testlines = fopen.readlines()
  # ignoring the first line
  knn_testing(karg[1],testlines[1:],karg[3])

main(sys.argv) # final submission