import pickle

# adds the liwc vectors to song data

def main():

	song_data = pickle.load(open('revised_songdata.pickle','rb'))

	complete_song_data = {}

	with open('liwc_results.txt', 'r') as f:
		topline = f.readline().split('\t')
		for line in f:
			line = line.split('\t')
			song_id = int(line[0].split('.')[0])
			liwc_vector = {}
			for i in range(2, len(topline)):
				liwc_vector[topline[i]] = line[i]
			song_info = list(song_data[song_id])			# song_info is a big tuple, this way list can be changed
			song_info.append(liwc_vector)
			complete_song_data[song_id] = song_info
	print(len(complete_song_data))
	with open('songdata_liwc.pickle','wb') as f:
		pickle.dump(complete_song_data,f)

main()