"""
Takes in tracks from util.py, writes them to json file for future use
"""

import json
import itertools
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import util

CLIENT_ID="810e2eec841546269c49f338f1be189a"
CLIENT_SECRET="764290d0ab0f4f4484b0d4c7b701bdee"
DATA_PATH = "data/tracks_5kalbums.json"
TRACK_TO_ARTIST_DICT_PATH = "data/track_to_artist_5kalbums.json"

def write_tracks_from_albums(sp):
    tracks = util.tracks_from_albums(sp, 2018, 5000)
    tracks.sort()
    tracks = list(s for s,_ in itertools.groupby(tracks)) # Remove duplicates
    with open(DATA_PATH,'w') as ff:
        json.dump(tracks, ff )

def write_track_to_artistid_dict(sp, read_path, write_path):
    with open(read_path,'r') as ff:
        songs = json.load(ff)
        dict = util.track_to_artistid_dict(sp, songs)
        with open(write_path, 'w') as ff:
            json.dump(dict, ff, sort_keys=True, indent=4)

def write_artist_to_feature_dict(sp, read_path, write_path):
    """
    read_path is a dictionary from songs to artist_ids
    """
    with open(read_path, 'r') as infile:
        track_artist_dict = json.load(infile)
        unique_artist_ids = set(track_artist_dict.values())
        artist_feature_dict = util.artistid_to_features_dict(sp, unique_artist_ids)
        with open(write_path, 'w') as outfile:
            json.dump(artist_feature_dict, outfile, sort_keys=True, indent=4)

if __name__ == "__main__":
    token = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    cache_token = token.get_access_token()
    sp = spotipy.Spotify(cache_token)
    write_track_to_artistid_dict(sp, DATA_PATH, TRACK_TO_ARTIST_DICT_PATH)
