#!/usr/bin/env python
import argparse, collections, itertools, math, os.path, re, string, operator
import nltk.data
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.corpus import movie_reviews, stopwords
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.util import ngrams
from nltk.metrics import BigramAssocMeasures, f_measure, masi_distance, precision, recall

#Sentiment analysis Trainer 
#Author Pratik Somanagoudar


### Corpus Building ###
#Corpus to load from
review_corpus = movie_reviews

isfilter_stopwords = True
isngrams = True
instance = 'paras'

ngram = [1,2]

count_value = 'bool'  # else it can be 'int'
debug = False
filter_stopwords = False
filter_stopwords_file = ""

### Reduce Features ###
is_min_score = True
is_max_feat = False
min_score = 1
max_feats = -1

DIVIDING_FRACTION = 0.75


### corpus Reader ###

#loading the corpus
print 'loading %s' % review_corpus
labels = review_corpus.categories()


print 'Cloud Flix Trainer'

# load stopwords 
if filter_stopwords == False:
	stopset = set()
else:
	stopset = set(stopwords.words(filter_stopwords_file))

# method for extracting words 
def norm_words(words):
	
	# get words lower case
	words = [w.lower() for w in words]
	# strip punctuations
	words = [w.strip(string.punctuation) for w in words]
	words = [w for w in words if w]
	
	if stopset:
		words = [w for w in words if w.lower() not in stopset]
	# in case nothing has happened to words, ensure is a list so can add together
	if not isinstance(words, list):
		words = list(words)
	# N-Gram words
	if ngrams:
		return reduce(operator.add, [words if n == 1 else ngrams(words, n) for n in ngram])
	else:
		return words


# Choose score Function
score_fn=BigramAssocMeasures.chi_sq

# calculate word score
def sum_category_word_scores(categorized_words, score_fn):
	# get word freq 
	word_fd = FreqDist()
	# get conditional freq Dist
	category_word_fd = ConditionalFreqDist()
	# according to catagory
	for category, words in categorized_words:
		for word in words:
			word_fd.inc(word)
			category_word_fd[category].inc(word)
	
	scores = collections.defaultdict(int)
	n_xx = category_word_fd.N()
	
	for category in category_word_fd.conditions():
		n_xi = category_word_fd[category].N()
		
		for word, n_ii in category_word_fd[category].iteritems():
			n_ix = word_fd[word]
			scores[word] += score_fn(n_ii, (n_ix, n_xi), n_xx)
	# return the scores
	return scores

# sorcted word socre
def sorted_word_scores(wsdict):
	return sorted(wsdict.items(), key=lambda (w, s): s, reverse=True)
# bag of words
def bag_of_words(words):
	return dict([(word, True) for word in words])

def bag_of_words_in_set(words, wordset):
	return bag_of_words(set(words) & wordset)

def word_counts(words):
	return dict(probability.FreqDist((w, 1) for w in words))

def word_counts_in_set(words, wordset):
	return word_counts((w for w in words if w in wordset))

def category_words(review_corpus):
	for category in review_corpus.categories():
		yield category, review_corpus.words(categories=[category])

def category_fileidset(review_corpus, category):
	return set(review_corpus.fileids(categories=[category]))

def category_sent_words(review_corpus, category):
	return review_corpus.sents(categories=[category])

def category_para_words(review_corpus, category):
	for para in review_corpus.paras(categories=[category]):
		yield itertools.chain(*para)

def category_file_words(categorized_corpus, category):
	for fileid in category_fileidset(categorized_corpus, category):
		yield categorized_corpus.words(fileids=[fileid])

### Feature Restriction ####

if is_min_score or is_max_feat:
	
	print 'calculating word scores'
	
	cat_words = [(cat, norm_words(words)) for cat, words in category_words(review_corpus)]
	ws = sorted_word_scores(sum_category_word_scores(cat_words, score_fn))
	
# if restricted to word score
	if is_min_score:
		ws = [(w, s) for (w, s) in ws if s >= min_score]

# if restricted to no of features
	if is_max_feat:
		ws = ws[:max_feats]

# bestwords	
	bestwords = set([w for (w, s) in ws])
	
	if count_value == 'bool':
	
		print 'using bag of words from known set feature extraction'
		
		featx = lambda words: bag_of_words_in_set(words, bestwords)
	else:
		
		print 'using word counts from known set feature extraction'
		
		featx = lambda words: word_counts_in_set(words, bestwords)
	
	if debug:
		print '%d words meet min_score and/or max_feats' % len(bestwords)
elif count_value == 'bool':
	
	print 'using bag of words feature extraction'
	
	featx = bag_of_words
else:
	
	print 'using word counts feature extraction'
	
	featx = word_counts

### Train and Test set creation ####

print 'Creating test and training set'

# Method to create training set.	
def train_test_feats(label, instances, featx=bag_of_words, fraction=0.75):
	labeled_instances = [(featx(i), label) for i in instances]
	
	if fraction != 1.0:
		l = len(instances)
		cutoff = int(math.ceil(l * fraction))
		return labeled_instances[:cutoff], labeled_instances[cutoff:]
	else:
		return labeled_instances, labeled_instances
# label instances
label_instance_function = {
		'sents': category_sent_words,
		'paras': category_para_words,
		'files': category_file_words
	}
# label function
lif = label_instance_function[instance]
label_instances = {}

# label catagorization	
for label in labels:
	instances = [norm_words(i) for i in lif(review_corpus, label)]
	label_instances[label] = [i for i in instances if i]
	
train_feats = []
test_feats = []
	
# create the two sets - training and test	
for label, instances in label_instances.iteritems():
		ltrain_feats, ltest_feats = train_test_feats(label, instances, featx=featx, fraction=DIVIDING_FRACTION)
		
		
		info = (label, len(ltrain_feats), len(ltest_feats))
		print '%s: %d training instances, %d testing instances' % info
		
		train_feats.extend(ltrain_feats)
		test_feats.extend(ltest_feats)
	

print '%d training feats, %d testing feats' % (len(train_feats), len(test_feats))
		

######TRAINING#########


# train the Naive Bayes Classifier	
print 'training NaiveBayes classifier'

classifier = NaiveBayesClassifier.train(train_feats)
    

print 'Training successful !!'

###EVALUATION#####

try:
	print 'accuracy: %f' % accuracy(classifier, test_feats)
except ZeroDivisionError:
	print 'accuracy: 0'

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
 
for i, (feats, label) in enumerate(test_feats):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)
 
print 'accuracy:', nltk.classify.util.accuracy(classifier, test_feats)
print 'pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
print 'pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])
print 'neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg'])
print 'neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg'])
classifier.show_most_informative_features()


#### PICKLE #####

# stoing the model
print 'Saving model ....'
def dump_object(object,name):
	import pickle
	f = open(name+'.pickle', 'wb')
	pickle.dump(object, f,1)
	f.close()


name = 'CloudFlix_NaiveBayes_Classifier'
fname = os.path.join(os.path.expanduser('~/nltk_data/classifiers'), name)		
dump_object(classifier, fname)

print 'Model is saved and ready to use.'