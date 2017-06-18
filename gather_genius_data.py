from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import sys
import json
import pickle


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def scrapeLyrics(page_url):
	# Script from: https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
	page = requests.get(page_url)
	html = BeautifulSoup(page.text, "html.parser")
	#remove script tags that they put in the middle of the lyrics
	[h.extract() for h in html('script')]
	#at least Genius is nice and has a tag called 'lyrics'!
	return html.find("div", { "class" : "lyrics" }).get_text()
	#return html.find("lyrics").get_text() this line didn't work when expanding the data

def findSongData(song_id):
	url = "http://api.genius.com/songs/" + str(song_id)
	headers = {'Authorization': 'Bearer Wo82Q4xkR7fMncKBWAIGVxsQkpdnA3kGvSUYa6s1RM9P1Kpha53GPzpb5y6C62lX'}
	response = requests.get(url, headers=headers)
	song_json = response.json()
	return song_json["response"]["song"]["title"], song_json["response"]["song"]["primary_artist"]["name"], song_json["response"]["song"]["url"]

def searchSong(song_title, artist_name):
	base_url = "http://api.genius.com"
	headers = {'Authorization': 'Bearer Wo82Q4xkR7fMncKBWAIGVxsQkpdnA3kGvSUYa6s1RM9P1Kpha53GPzpb5y6C62lX'}
	search_url = base_url + "/search"
	data = {'q': song_title}
	response = requests.get(search_url, params=data, headers=headers)
	result_json = response.json()
	for hit in result_json["response"]["hits"]:
		if hit["result"]["primary_artist"]["name"] == artist_name:
			return hit["result"]["id"]
		elif hit["result"]["primary_artist"]["name"] in artist_name:
			return hit["result"]["id"]
	return 0

def ArtistIsSongwriter(song_id, artist):
	url = "http://api.genius.com/songs/" + str(song_id)
	headers = {'Authorization': 'Bearer Wo82Q4xkR7fMncKBWAIGVxsQkpdnA3kGvSUYa6s1RM9P1Kpha53GPzpb5y6C62lX'}
	response = requests.get(url, headers=headers)
	song_json = response.json()
	for sw in song_json["response"]["song"]["writer_artists"]:
		if artist == sw["name"]:
			return 1
	return 0

def searchMultipleSongs(artist_id, writer):
	print("##### Finding songs for ", writer)
	base_url = "http://api.genius.com/artists/"
	headers = {'Authorization': 'Bearer Wo82Q4xkR7fMncKBWAIGVxsQkpdnA3kGvSUYa6s1RM9P1Kpha53GPzpb5y6C62lX'}
	search_url = base_url + str(artist_id) + "/songs?per_page=50"
	response = requests.get(search_url, headers=headers)
	result_json = response.json()
	song_data = {}
	for song in result_json["response"]["songs"]:
		song_id = song["id"]
		if '[' not in song["title"]:
			if ArtistIsSongwriter(song_id, writer):
				song_data[song_id] = writer	# If artist is songwriter, but on someone elses song, still include
	return song_data

def main():
	# Find data for artists that write own songs
	writing_artists = {1177:'Taylor Swift', 12418:'Ed Sheeran', 130:'Drake', 2197:'Future', 69:'J. Cole'}

	song_data = {}
	for artist in writing_artists:
		song_data.update(searchMultipleSongs(artist, writing_artists[artist]))
	print(song_data)
	# complete song data
	# search for title, lyrics

	# Find song data for txt files
	official_songwriters = {"bennyblanco.txt":"Benny Blanco", "cirkut.txt":"Cirkut", "shellback.txt":"Shellback"}
	for fname in official_songwriters:
		print("##### Searching songs for file: ", fname)
		with open(fname) as f:
			for line in f:
				line = line.split('\t')
				song_id_found = searchSong(line[0], line[1])
				if song_id_found:
					if ArtistIsSongwriter(song_id_found, official_songwriters[fname]):
						if song_id_found not in song_data:
							song_data[song_id_found] = official_songwriters[fname]
	print("##### Backing up song data")
	with open('songdata_backup.pickle','wb') as f:
		pickle.dump(song_data,f)
	# Use this backup if you dont have enough time to run script at once
	#song_data = pickle.load(open('songdata_backup.pickle','rb'))

	# After this step, we have a dictionary with song ids as keys, and a one-item-list with the songwriter
	# Now we need to complete our data, so lets get everything from genius we need
	print("##### Completing song data", len(song_data))
	count = 0
	for song in song_data:
		count+=1
		print(count)
		sw = song_data[song]
		title, artist, url = findSongData(song)
		print(title, artist, url)
		lyrics = scrapeLyrics(url)
		song_data[song] = [title, artist, sw, lyrics]

	# Now we have all our (extra) data for these 8 artists/songwriters
	# Lets combine these with the ones from the older data set
	print("##### Combining data sets")
	old_song_data = pickle.load(open('complete_song_data.pickle','rb'))

	for s in old_song_data:
		sws_old = old_song_data[s][2]
		sws = list(writing_artists.values())
		for sw in sws_old:
			if sw in sws:
				if s not in song_data:
					song_data[s] = old_song_data[s][0], old_song_data[s][1], sw, old_song_data[s][3]

	for song in song_data:
		print("{:10} {:40} {:40} {:40} {}".format(song, song_data[song][0], song_data[song][1], song_data[song][2], song_data[song][3][:10]))

	with open('songdata.pickle','wb') as f:
		pickle.dump(song_data,f)


main()