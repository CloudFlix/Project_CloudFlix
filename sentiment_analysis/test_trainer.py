import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
 
### Corpus Building ###
review_corpus = movie_reviews
isfilter_stopwords = True
isngrams = True


ngram = [1,2]

count_value = 'bool'  # else it can be 'int'
debug = False
filter_stopwords = False


### Reduce Features ###
is_min_score = True
is_max_feat = False
min_score = 0
max_feats = -1

DIVIDING_FRACTION = 3/4

 
def evaluate_classifier(featx):
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')
 
    negfeats = [(featx(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(featx(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
 
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
 
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print 'training ....'
    classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
 
    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
 
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    print 'pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])
    print 'neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg'])
    classifier.show_most_informative_features()

def word_feats(words):
    return dict([(word, True) for word in words])
 

def norm_words(words):
    
    words = [w.lower() for w in words]
    
    words = [w.strip(string.punctuation) for w in words]
    words = [w for w in words if w]
    
    if stopset:
        words = [w for w in words if w.lower() not in stopset]
    # in case nothing has happened to words, ensure is a list so can add together
    if not isinstance(words, list):
        words = list(words)
    
    if isngrams:
        return reduce(operator.add, [words if n == 1 else ngrams(words, n) for n in ngram])
    else:
        return words

evaluate_classifier(word_feats)