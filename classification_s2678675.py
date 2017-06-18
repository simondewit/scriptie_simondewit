#!/usr/bin/python2.7
# Program that uses bag of words classification to classify song lyrics
# Partly based on script provided by course Information Retrieval 2017

from nltk.tokenize import RegexpTokenizer
import nltk.classify
from nltk.tokenize import word_tokenize
from featx import bag_of_words, high_information_words, bag_of_words_in_set
from classification import precision_recall
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from random import shuffle
from os import listdir # to read files
from os.path import isfile, join # to read files
import sys
import pickle

# Return all the filenames in a folder
def get_filenames_in_folder(folder):
	return [f for f in listdir(folder) if isfile(join(folder, f))]

# Reads all the files that correspond to the input list of categories and puts their contents in bags of words
def read_files():
	feats = list ()
	print("\n##### Reading files...")
	song_data = pickle.load(open('final_songdata2.pickle','rb'))
	files = get_filenames_in_folder('lyric_files')
	num_files=0
	for f in files:
		data = open('lyric_files/' + f, 'r').read()
		song_id = int(f.split(".")[0])
		songwriter = song_data[song_id][2]

		# Remove all punctuation
		customTokenizer = RegexpTokenizer(r'\w+')
		tokens = customTokenizer.tokenize(data)

		# Lowercase everything
		tokens = [t.lower() for t in tokens]
		bag = bag_of_words(tokens)
		feats.append((bag, songwriter))
		num_files+=1

	return feats

# Splits a labelled dataset into two disjoint subsets train and test
def split_train_test(feats, split=0.9):
	train_feats = []
	test_feats = []

	shuffle(feats) # randomise dataset before splitting into train and test
	cutoff = int(len(feats) * split)
	train_feats, test_feats = feats[:cutoff], feats[cutoff:]	

	print("\n##### Splitting datasets...")
	print("  Training set: %i" % len(train_feats))
	print("  Test set: %i" % len(test_feats))
	return train_feats, test_feats

# Trains a classifier
def train(train_feats):
	classifier = nltk.classify.NaiveBayesClassifier.train(train_feats)
	return classifier

# Calculates F-score
def calculate_f(precisions, recalls, categories):
	f_measures = {}
	for category in categories:
		try:
			f_measures[category] = round((2 * (precisions[category] * recalls[category])) / (precisions[category] + recalls[category]), 6)
		except TypeError:
			f_measures[category] = 0.0
		except ZeroDivisionError:
			f_measures[category] = 0.0
	return f_measures

# Prints accuracy, precision and recall
def evaluation(classifier, test_feats, categories):
	print ("\n##### Evaluation...")
	accuracy = nltk.classify.accuracy(classifier, test_feats)
	precisions, recalls = precision_recall(classifier, test_feats)
	f_measures = calculate_f(precisions, recalls, categories)  

	print(" |-------------|-----------|-----------|-----------|")
	print(" |%-13s|%-11s|%-11s|%-11s|" % ("category","precision","recall","F-measure"))
	print(" |-------------|-----------|-----------|-----------|")
	for category in categories:
		if precisions[category] is None or recalls[category] is None:
			print(" |%-13s|%-11s|%-11s|%-11s|" % (category, "NA", "NA", "NA")) 
		else:
			print(" |%-13s|%-11f|%-11f|%-11s|" % (category, precisions[category], recalls[category], f_measures[category]))
	print(" |-------------|-----------|-----------|-----------|")
	return accuracy




# Show informative features
def analysis(classifier):
	print("\n##### Analysis...")
	classifier.show_most_informative_features(10)

# Obtain the high information words
def high_information(feats, categories):
	print("\n##### Obtaining high information words...")

	labelled_words = [(category, []) for category in categories]

	from collections import defaultdict
	words = defaultdict(list)
	all_words = list()
	for category in categories:
		words[category] = list()

	for feat in feats:
		category = feat[1]
		bag = feat[0]
		for w in bag.keys():
			words[category].append(w)
			all_words.append(w)

	labelled_words = [(category, words[category]) for category in categories]
	high_info_words = set(high_information_words(labelled_words, min_score=12))

	print("  Number of words in the data: %i" % len(all_words))
	print("  Number of distinct words in the data: %i" % len(set(all_words)))
	print("  Number of distinct 'high-information' words in the data: %i" % len(high_info_words))

	return high_info_words

def high_info_feats(feats,hiw):
	""" Function that takes the generated feats for all files, and only returns the 
		matching high information words for every file in the same format as feats
	"""
	hif = []
	for tup in feats:
		new_feats = {}
		cat = tup[1]
		tokens = set(tup[0].keys())
		high_info_tokens = bag_of_words_in_set(tokens, hiw)
		for t in high_info_tokens:
			new_feats[t] = True
		hif.append((new_feats,cat))
	return hif

def main():
	categories = ["Shellback", "Benny Blanco", "Cirkut", "Ed Sheeran", "Taylor Swift", "Drake", "Future", "J. Cole"]
	feats = read_files()
	high_info_words = high_information(feats, categories)
	new_hiw = high_info_feats(feats,high_info_words)

	accuracies = []
	for N in range(10):
		train_feats, test_feats = split_train_test(new_hiw)
		classifier = train(train_feats)
		accuracies.append(evaluation(classifier, test_feats, categories))
		analysis(classifier)
	for acc in accuracies:
		print(acc)
	print(sum(accuracies)/len(accuracies))

if __name__ == "__main__":
	main()



