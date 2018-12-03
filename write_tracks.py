"""
Takes in tracks from util.py, writes them to json file for future use
"""

import json
import itertools

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import util

DATA_PATH = "data/tracks_5kalbums.json"

if __name__ == "__main__":
    CLIENT_ID="810e2eec841546269c49f338f1be189a"
    CLIENT_SECRET="764290d0ab0f4f4484b0d4c7b701bdee"
    token = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    cache_token = token.get_access_token()
    sp = spotipy.Spotify(cache_token)

    tracks = util.tracks_from_albums(sp, 2018, 5000)
    # Remove duplicates
    tracks.sort()
    tracks = list(s for s,_ in itertools.groupby(tracks))
    #Write to file
    with open(DATA_PATH,'w') as ff:
        json.dump(tracks, ff )
