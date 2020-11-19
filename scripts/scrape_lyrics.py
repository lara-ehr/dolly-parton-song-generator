import requests
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

URL_BASE = 'https://www.lyrics.com/artist/'

CORPUS_DIRECTORY = '../corpus/'

def get_artist_string(raw):
    '''
    Takes user input and joins with hyphen
    '''
    new = raw.split(' ')
    new = '-'.join(new)
    return new

def make_artist_url(new):
    '''
    Generates URL for web scraping
    '''
    url = f'{URL_BASE}{new}'
    return url

def get_song_list(artist, url, artist_path):
    list_of_song_urls = []
    request = requests.get(url)
    soup = BeautifulSoup(request.text, features="lxml")
    with open(f'{artist_path}/_All_Songs_{artist}.txt', 'w') as f: # create the new files within the new directory
        for link in soup.body.find_all(class_ = 'tal qx'):
            song = link.find('a').get('href')
            songname = link.find('a').get_text()
            song_url = 'http://www.lyrics.com'+ str(song) + '\n'
            list_of_song_urls.append(songname + '\t' + song_url)
        f.writelines(list_of_song_urls)

def get_lyrics(artist_path, artist):
    all_songs = open(f'{artist_path}/_All_Songs_{artist}.txt', 'r').read().split('\n')
    all_titles = []
    for line in all_songs[:-1]: # need to index to penultimate line as there is a newline at the end of the file.
        song_title = line.split('\t')[0]
        song_title = re.sub('\W', '', song_title)
        if song_title not in all_titles:
            all_titles.append(song_title)
            song_link = line.split('\t')[1]
            with open(f'{artist_path}/{artist}_{song_title}.txt', 'w') as f:
                request_lyrics = requests.get(str(song_link))
                soup_lyrics = BeautifulSoup(request_lyrics.text, features="lxml")
                lyrics = soup_lyrics.pre.get_text()
                f.writelines(lyrics)


if __name__ == "__main__":

    artist_raw = input('Which artist(s) are you interested in?')
    artist = get_artist_string(artist_raw)
    url = make_artist_url(artist)

    artist_path = CORPUS_DIRECTORY+artist
    os.mkdir(artist_path)

    get_song_list(artist, url, artist_path)
    get_lyrics(artist_path, artist)
