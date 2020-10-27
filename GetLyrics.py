from bs4 import BeautifulSoup
import requests
import argparse
import re

import spotipy
import spotipy.util as util

class GetLyrics:

    def activate_spotify(self):

        #To create your token you have to get client-id and secret you have to login as developer and create project.

        user = "" # INSERT YOUR USER ID -> https://www.spotify.com/(your country shortcut)/account/overview -> username section
        cid = "" # INSERT YOUR CLIENT ID -> http://developer.spotify.com/dasboard/applications/clientid -> "Create an App" -> Copy the client id here.
        scope = "user-read-currently-playing"
        secret = "" # INSERT YOUR SECRET ID (and don't share it with people)-> https://developer.spotify.com/dashboard/applications/clientid -> "Show Client Secret" -> Copy it to here.
        uri = "https://127.0.0.1:8888/callback" # You have to press edit settings and give this value to redirest URL's part. Then click add.
        token = util.prompt_for_user_token(username=user,
                                           scope=scope,
                                           client_id=cid,
                                           client_secret=secret,
                                           redirect_uri=uri)

        sp = spotipy.Spotify(auth=token) # Object initiated with your special token.
        current_song = sp.currently_playing()
        artist = str(current_song['item']['artists'][0]['name']).replace(" ", "").lower()
        song = str(current_song['item']['name']).replace(" ", "").lower()
        return artist, song

    def arg_parse(self):
        parser = argparse.ArgumentParser(description="A commandline helper to fetch lyrics.")
        parser.add_argument("-a", "--artist", type=str, action="store", dest="artist", help="Enter artist.")
        parser.add_argument("-s", "--song", type=str, action="store", dest="song", help="Enter song name.")
        args = parser.parse_args()
        
        regex  = re.compile('[^a-zA-Z0-9]')
        
        artist = regex.sub('',str(args.artist)).lower()
        song = regex.sub('',str(args.song)).lower()
        return artist, song

    def send_request(self, artist, song):
        # Language spesific songs, # including artist name or song with symbols and language characteristic characters can cause it to return empty.
        # It is because of the website I get lyrics from. IT is work in progress. If I find better much stable alternative I will switch to it.
        url = "https://www.azlyrics.com/lyrics/" + artist + "/" + song + ".html"
        request = requests.get(url)
        soup = BeautifulSoup(request.content, "lxml")
        result = soup.find_all("div", {"class": "col-xs-12 col-lg-8 text-center"})
        result2 = ""

        for iterate in result:
            result2 = iterate.find_all("div")[5].text

        print(result2)

