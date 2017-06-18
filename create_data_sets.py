import pickle
from scipy import spatial

def main():

	songwriters = pickle.load(open('songwriters.pickle','rb'))
	song_data = pickle.load(open('final_songdata2.pickle','rb'))

	# Now we need to create a training and test set
	# First we create the training set
	songs_training = []
	songs_testing = []
	songwriters_training = {}
	songwriters_testing = {}
	for sw in songwriters:
		# Create a list with song ids for training and testing per song writer, so I can create a train and test pickle
		train_ids = songwriters[sw][:int(len(songwriters[sw])*0.9)]
		test_ids = list(set(songwriters[sw]).difference(train_ids))
		songwriters_training[sw] = train_ids
		songwriters_testing[sw] = test_ids
		songs_training.extend(train_ids)
		songs_testing.extend(test_ids)

	testing_songdata = {}
	for song in songs_testing:
		testing_songdata[song] = song_data[song]

	with open('songwriters_train.pickle','wb') as f:
		pickle.dump(songwriters_training,f)

	with open('songwriters_test.pickle','wb') as f:
		pickle.dump(songwriters_testing,f)

	with open('songdata_testing.pickle','wb') as f:
		pickle.dump(testing_songdata,f)


main()

