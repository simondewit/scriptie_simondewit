import pickle
import nltk

# This script calculates the lyric dependent features

def searchChorus(lyric):
	# This function finds al choruses/hooks and stores the complete chorus as item in a list
	option1, option2 = "[chorus", "[hook"
	save = 0
	choruses = []
	chorus = []
	for line in lyric.split('\n'):
		if option1 in line.lower() or option2 in line.lower():
			save = 1
			chorus = []
		elif '[' in line and chorus != []:
			save = 0
			choruses.append(" ".join(chorus[1:-1]))
			chorus = []
		if save:
			chorus.append(line)
	return choruses

def searchVerses(lyric):
	option1 = "[verse"
	save = 0
	verses = []
	verse = []
	for line in lyric.split('\n'):
		if option1 in line.lower():
			save = 1
			verse = []
		elif '[' in line and verse != []:
			save = 0
			verses.append(" ".join(verse[1:-1]))
			verse = []
		if save:
			verse.append(line)
	return verses

def searchBridge(lyric):
	return 1 if lyric.lower().count("[bridge") else 0

def typeToken(txt):
	tokens = nltk.word_tokenize(txt)
	types = set(tokens)
	return (len(types), len(tokens))

def avgTypeToken(l):
	# Calculates the avg type and avg tokens
	avg_types, avg_tokens = 0, 0
	if l != []:
		for item in l:
			types, tokens = typeToken(item)
			avg_types += types
			avg_tokens += tokens
		return (avg_types/len(l), avg_tokens/len(l))
	return 0, 0

def main():

	song_data = pickle.load(open('songdata_liwc.pickle','rb'))

	for song in song_data:
		lyrics = song_data[song][3]
		# Type Token complete lyrics
		tt_lyrics = typeToken(lyrics)
		# Type / Token verse
		verses = searchVerses(lyrics)
		tt_verses = avgTypeToken(verses)
		# Avg words verse
		avg_words_verses = sum(len(v.split()) for v in verses)/len(verses) if len(verses) else 0
		# Type / Token chorus
		chorus = searchChorus(lyrics)
		tt_chorus = avgTypeToken(chorus)
		# Avg words chorus
		avg_words_chorus = sum(len(c.split()) for c in chorus)/len(chorus) if len(chorus) else 0
		isBridge = searchBridge(lyrics)
		print("SONG: ", song)
		print("TT LYRICS ", tt_lyrics)
		print("TT VERSES ", tt_verses)
		print("TT CHORUSES ", tt_chorus)
		print("AVG WORDS VERSE ", avg_words_verses)
		print("AVG WORDS CHORUS ", avg_words_chorus)
		print("BRIDGE?", isBridge)
		song_data[song].extend([tt_lyrics, tt_verses, tt_chorus, avg_words_verses, avg_words_chorus, isBridge])
		
		with open('final_songdata.pickle','wb') as f:
			pickle.dump(song_data,f)

main()