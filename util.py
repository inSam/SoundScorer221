"""
A collection of utility methods, primarily used for interfacing with Spotipy APIself.
In particular, these are methods typically used for randomly sampling from Spotipy data

Lists of tracks are returned in our standard format:
[(song id, song name, popularity)]

We currently use tracks_from_albums(sp, year, num_albums) to randomly sample
"""

from time import sleep

def extract_songs(sp, playlist):
    """Get (song id, song name, popularity) out of playlists

    @param sp : Spotipy client
    @param playlist: ID for Spotipy playlist

    """
    tracks = playlist["tracks"]
    info = [(item["track"]["id"], item["track"]["name"], item["track"]["popularity"]) for item in tracks["items"]]
    while tracks["next"]:
        tracks = sp.next(tracks)
        info.extend([(item["track"]["id"], item["track"]["name"], item["track"]["popularity"]) for item in tracks["items"]])
    return info

def tracks_from_year(sp, year, num_tracks):
    """
    # Get (song_id, song_name, popularity) for num_tracks songs in given year
    # Goes through songs sequentially to get tracks
    """
    tracks = sp.search(q='year:' + str(year), type='track', offset=0, limit=50)
    print("Number of tracks in {}: {}".format(year, tracks['tracks']['total']))
    info = [(item["id"], item["name"], item["popularity"]) for item in tracks["tracks"]["items"]]
    while tracks["tracks"]["next"] and len(info) < num_tracks:
        tracks = sp.next(tracks["tracks"])
        info.extend([(item["id"], item["name"], item["popularity"]) for item in tracks["tracks"]["items"]])
        if len(info) % 1000 == 0:
            print("Retrieved {} songs".format(len(info)))
    return info[:num_tracks]


def random_tracks_from_year(sp, year, num_tracks):
    """
    # Get (song_id, song_name, popularity) for num_tracks songs in a given year
    # Selects those songs randomly from the given year's top 10,000
    """
    tracks = sp.search(q='year:' + str(year), type='track')
    print("Number of tracks in {}: {}".format(year, tracks['tracks']['total']))
    max_track = min(tracks['tracks']['total'], 9999) # Spotify limits offset to 9999
    infos = []
    for _ in range(num_tracks):
        track_num = random.randint(1, max_track) # May repeat songs
        result = sp.search(q='year:' + str(year), type='track', offset=track_num, limit=1)
        track = result['tracks']['items'][0]
        info = (track['id'], track['name'], track['popularity'])
        infos.append(info)
    return infos

def album_ids_from_year(sp, year, num_albums):
    """
    Get the top num_albums album IDs from given year
    """
    albums = sp.search(q='year:' + str(year), type='album', offset=0, limit=50)
    print("Number of albums in {}: {}".format(year, albums['albums']['total']))
    album_ids = [item['id'] for item in albums["albums"]["items"]]
    while albums["albums"]["next"] and len(album_ids) < num_albums:
        albums = sp.next(albums["albums"])
        album_ids.extend([item['id'] for item in albums["albums"]["items"]])
        if len(albums) % 1000 == 0:
            print("Retrieved {} album IDs".format(len(albums)))
    return album_ids[:num_albums]

def tracks_from_albums(sp, year, num_albums):
    """
    Return list of song info from list of albums
    """
    album_ids = album_ids_from_year(sp, year, num_albums)
    print("Pulled {} albums".format(num_albums))
    info = []
    for i, album_id in enumerate(album_ids):
        try:
            sleep(0.1)
            album = sp.album(album_id)
            track_ids = [item["id"] for item in album["tracks"]["items"]]
            for tid in track_ids:
                sleep(0.1)
                track = sp.track(tid)
                info.append((track["id"], track["name"], track["popularity"]))
        except:
            print("Caught Spotipy error - breaking out of API calls")
            break
        if len(info) % 100 == 0:
            print("Retrieved {} songs".format(len(info)))
        if i % 50 == 0:
            print("Retrived songs from {} albums".format(i))
    print("{} songs retrieved from {} albums".format(len(info), len(album_ids)))
    return info

def track_to_artistid_dict(sp, tracks):
    """
    Given list of track_ids
    returns dictionary from all track_ids to artist IDs
    """
    track_artist_dict = {}
    for i in range(0, len(tracks), 50):
        track_ids = tracks[i : i + 50]
        track_infos = sp.tracks(track_ids)["tracks"]
        assert len(track_ids) == len(track_infos)
        for track_id, info in zip(track_ids, track_infos):
            if not info:
                continue # song not found in Spotify
            track_artist_dict[track_id] = info["artists"][0]["id"]
        if len(track_artist_dict) % 100 == 0:
            print("Stored {} artist IDs".format(len(track_artist_dict)))
            print(list(track_artist_dict.items())[0])
    return track_artist_dict

def artistid_to_features_dict(sp, artist_ids):
    """
    Given iterable of artist_ids, returns a map from artist_id to feature_dict for each artist
    e.g. {"093sDFBR924": {"followers" : 1038, "genres": ["pop", "rock"]},
            "RV3910FWS": {"followers" : 31001, "genres": ["country"]}
    """
    feature_dict = {}
    unique_ids = set(artist_ids)
    for artist_id in unique_ids:
        artist = sp.artist(artist_id)
        feature_dict[artist_id] = {
            "followers": artist["followers"]["total"],
            "popularity": artist["popularity"],
            "genres": artist["genres"]
        }
    return feature_dict
