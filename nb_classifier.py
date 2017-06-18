import pickle
import nltk
import random
from classification_s2678675 import evaluation

# Naive Bayes classification with LIWC values and lyric dependent values

def addFeatureToDict(d, feature, value):
	d[feature] = value
	return d

def pickFeatures(d):
	# Original features
	# features = ["posemo", "sexual", "affiliation", "money", "Authentic", "swear", "body", "anger", "affect"
	# "Tone", "relig", "Clout", "insight", "netspeak", "Analytic", "nonflu", "you", "i", "feel"]
	features = ["Authentic", "Analytic"]

	feats_dict = {}
	for feat in d:
		if feat in features:
			feats_dict[feat] = d[feat]
	return feats_dict

def main():

	song_data = pickle.load(open('final_songdata2.pickle','rb'))
	songwriters = pickle.load(open('songwriters.pickle','rb'))

	#Train 10 times
	accuracies = []
	for i in range(10):
		training = []
		testing = []
		# Create 2 lists with ids for training and testing 90/10
		for sw in songwriters:
			ids = songwriters[sw]
			random.shuffle(ids)
			training.extend(ids[:int(len(ids)*0.9)])
			testing.extend(list(set(ids).difference(training)))

		# Prepare list with tuples for training classifier
		nb_train = []
		for song in training:
			selected_features = {}
			# un comment to choos which values: liwc values or lyric dependent values
			# selected_features = pickFeatures(song_data[song][4])
			# selected_features = addFeatureToDict(selected_features, 'tt_chorus', song_data[song][7])
			selected_features = addFeatureToDict(selected_features, 'avg_verse', song_data[song][8])
			selected_features = addFeatureToDict(selected_features, 'avg_chorus', song_data[song][9])
			selected_features = addFeatureToDict(selected_features, 'bridge', song_data[song][10])
			nb_train.append((selected_features, song_data[song][2]))
			# nb_train.append((song_data[song][4], song_data[song][2]))

		# Prepare list with tuples for testing classifier
		nb_test = []
		for song in testing:
			selected_features = {}
			# un comment to choos which values: liwc values or lyric dependent values
			# selected_features = pickFeatures(song_data[song][4])
			# selected_features = addFeatureToDict(selected_features, 'tt_chorus', song_data[song][7])
			selected_features = addFeatureToDict(selected_features, 'avg_verse', song_data[song][8])
			selected_features = addFeatureToDict(selected_features, 'avg_chorus', song_data[song][9])
			selected_features = addFeatureToDict(selected_features, 'bridge', song_data[song][10])
			nb_test.append((selected_features, song_data[song][2]))
			#nb_test.append((song_data[song][4], song_data[song][2]))


		categories = ["Shellback", "Benny Blanco", "Cirkut", "Ed Sheeran", "Taylor Swift", "Drake", "Future", "J. Cole"]
		classifier = nltk.NaiveBayesClassifier.train(nb_train)
		accuracies.append(evaluation(classifier, nb_test, categories))
	for acc in accuracies:
		print(acc)
	print(sum(accuracies)/len(accuracies))

main()