from GetLyrics import GetLyrics
import sys

obj = GetLyrics()

if len(sys.argv) > 1:
    artist = obj.arg_parse()[0]
    song = obj.arg_parse()[1]

else:
    artist = obj.activate_spotify()[0]
    song = obj.activate_spotify()[1]

obj.send_request(artist, song)
