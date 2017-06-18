import pickle
import operator

# different approach on getting the songwriters, since the other way (picking the first one of each song) the artists are credited often, while they do not write (drake). 
# now im picking the songwriters who worked on most songs instead of the first one.

def main():
	songwriters = {}

	songs = pickle.load(open('song_data.pickle','rb'))

	for song in songs:
		fname = str(song) + ".txt"
		with open(fname,'w') as f:
			f.write(songs[song][3])

main()