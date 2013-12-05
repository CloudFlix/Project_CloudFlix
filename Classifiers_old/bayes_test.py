__author__ = 'Srikanth'
# Naive Bayes
import os,sys
import shlex
from collections import defaultdict
import string
import re
from random import shuffle
from collections import Counter
import math,cPickle as pickle
import string
from nltk import stem
from nltk.tokenize import RegexpTokenizer

def lambdafn_float():
  return defaultdict(float)

def multinomial_testing(modelfile,testlines,predictionfile):
  linecount = 0
  # cond_prob has the idf information as well
  [prior_dict, cond_prob, idf_dict,denomdict] = pickle.load( open( modelfile, "rb" ) )
  scorefile = open(predictionfile,"w")
  scorefile.write("Id,Category\n")
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

  for commentline in testlines:
    linecount += 1
    commentline = commentline.lower()
    commentline = commentline.replace("it's","it is")
    commentline = commentline.replace("won't","will not")
    commentline = commentline.replace("can't","cannot")
    commentline = commentline.replace("'ll"," will")
    commentline = commentline.replace("n't"," not")
    commentwords = tokenizer.tokenize(commentline)

    # identify exclusive numericalpha
    allnumkeys = [m.group(0) for word in commentwords for m in [exp_allnums.search(word)] if m ]
    wordnumset = [m.group(0) for word in set(commentwords)-set(allnumkeys) for m in [exp_wordnums.search(word)] if m ]
    numwordset = [m.group(0) for word in set(commentwords)-set(allnumkeys)-set(wordnumset) for m in [exp_numwords.search(word)] if m ]

    commentwords = [stemmer.stem(x) for x in commentwords if stemmer.stem(x) not in set(stopwords)|set(allnumkeys)|set(wordnumset)|set(numwordset)]

    scoredict = defaultdict(float)
    for cl in [0,1]:
      scoredict[cl] =math.log(prior_dict[cl],2)
      for word in commentwords:
        if cond_prob[cl][word] != 0:
          # word seen during training. word with idf this is giving reduced prob.
          #scoredict[cl] += math.log(cond_prob[cl][word]*idf_dict[word] ,2)
          scoredict[cl] += math.log(cond_prob[cl][word] ,2)

        else:
          # word not seen in training
          scoredict[cl] -= math.log(denomdict[cl],2) # this gave 76% score


    score = max(scoredict , key=scoredict.get)
    #print "hello", scoredict, score
    scorefile.write(str(linecount)+","+str(score)+"\n")
  scorefile.close()

def main(karg):
  # Script main file.
  if len(karg) !=4:
    print "Usage error: Use python test.py model_file test_file.csv prediction_file"
    sys.exit(0)

  fopen = open(karg[2])
  testlines = fopen.readlines()
  # ignoring the first line.
  multinomial_testing(karg[1],testlines[1:],karg[3])


main(sys.argv)