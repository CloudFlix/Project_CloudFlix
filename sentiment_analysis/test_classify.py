import nltk.data
from nltk.util import ngrams
import collections
import nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import os



# def word_feats(words):
#     return dict([(word, True) for word in words + ngrams(words, 2)])

classifier = nltk.data.load("classifiers/movie_reviews_NaiveBayes.pickle")

# print classifier.classify(feats)
count=0
neg_count = 0
pos_count = 0

for dirname, dirnames, filenames in os.walk('/Users/pratiksomanagoudar/Documents/movie_reviews/neg'):
    for filename in filenames:  
        with open(dirname+"/"+filename) as f:
            content = f.readlines()
            for line in content: 
            	count = count +1
                words=line.split(" ")
                feats = dict([(word, True) for word in words + ngrams(words, 2)])
                classe=classifier.classify(feats)
                if classe == 'neg':
                	neg_count= neg_count+1
                elif classe =='pos':
                	pos_count= pos_count+1

print count
print neg_count
print pos_count
