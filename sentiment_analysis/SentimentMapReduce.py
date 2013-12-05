'''
Created on Nov 12, 2013

@author: pratiksomanagoudar
'''
import collections
from mrjob.job import MRJob
from nltk.classify import NaiveBayesClassifier
import nltk.data
from nltk.util import ngrams


class SentimentMapReduce(MRJob):
    
    def mapper_sentiment(self, _, line):
        classifier = nltk.data.load("classifiers/movie_reviews_NaiveBayes.pickle")
        movieData = line.split('\t')
        reviews = movieData[1].split('||')
        
        for review in reviews:
            words=review.split(' ')
            feats = dict([(word, True) for word in words + ngrams(words, 2)])
            val = classifier.classify(feats)
            yield (movieData[0], val)


    def reducer_sentiment(self, movie, values):
        
        positiveCount=0
        negetiveCount=0
        total=0
        for value in values:
            total=total+1
            if value =='pos':
                positiveCount = positiveCount+1
            if value =='neg':
                negetiveCount = negetiveCount+1 
                   
        yield (movie,'{}||{}||{}'.format(positiveCount, negetiveCount,total))


    def steps(self):
        return [
           self.mr(mapper=self.mapper_sentiment,
                  reducer=self.reducer_sentiment)
#            self.mr(mapper=self.mapper_sentiment)
        ]

if __name__ == '__main__':
    SentimentMapReduce.run()
