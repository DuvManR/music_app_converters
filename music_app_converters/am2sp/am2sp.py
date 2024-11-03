from spotipy.oauth2 import SpotifyOAuth
import spotipy
import json
import sys
import os

# Spotify Constants
CID = '<YOUR-CLIENT-ID>'
SECRET = '<YOUR_API_SECRET>'
USER_ID = '<YOU_USER_ID>'
REDIRECT_URI = "http://localhost:5000"
SEARCH_QUERY = 'artist:%s track:%s'
SCOPE = "playlist-modify-public"
USERNAME = '<YOUR_USERNAME>'
SP_OBJ_TRACKS_KEY = 'tracks'
SP_OBJ_TRACK_TYPE = 'track'
SP_OBJ_ITEMS_KEY = 'items'
SP_OBJ_ID_KEY = 'id'
SP_NEW_PLAYLIST = 'AM > SP'

# Apple Music Constants
AM_OBJ_ARTIST_KEY = 'song_artist'
AM_OBJ_SONG_KEY = 'song_name'

# Logging Constants
ERROR_LOG = 'not_found.txt'


# Loads the data of the Apple Music playlist
def load_playlist_data():
    # PC
    with open(r'tracks.json', 'r', encoding='utf-8') as my_playlist_file:
        playlist_data_str = '[' + my_playlist_file.read() + ']'
        playlist_data = json.loads(playlist_data_str)
    return playlist_data

    # iPhone
    return '[' + sys.argv[1] + ']'


# Function that creates a Spotify playlist with the retrieved Apple Music tracks
def create_playlist(playlist_data, my_sp_user):
    # Creates a new Spotify playlist
    new_playlist_id = my_sp_user.user_playlist_create(user=USER_ID, name=SP_NEW_PLAYLIST)[SP_OBJ_ID_KEY]

    # Iterates over the retrieved Apple Music tracks, for each searching for an equivalent in Spotify.
    # If no track is found, writes an error log
    tracks2add = []
    for current_track in playlist_data:
        sp_search_result = my_sp_user.search(q=SEARCH_QUERY % (current_track[AM_OBJ_ARTIST_KEY].replace("'", ""), current_track[AM_OBJ_SONG_KEY].replace("'", "")), type=SP_OBJ_TRACK_TYPE, limit=1)[SP_OBJ_TRACKS_KEY][SP_OBJ_ITEMS_KEY]
        if sp_search_result:
            tracks2add += [sp_search_result[0][SP_OBJ_ID_KEY]]
        else:
            with open(ERROR_LOG, 'a') as not_found_file:
                not_found_file.write(str(current_track) + '\n')

    # Adds the retrieved Apple Music tracks which also found in Spotify to the newly created playlist
    my_sp_user.playlist_add_items(playlist_id=new_playlist_id, items=tracks2add)


# Clears the error log file
def remove_error_log_file():
    os.remove(ERROR_LOG)


# Initiates a Spotify connection
def sp_auth():
    client_credentials_manager = SpotifyOAuth(client_id=CID, client_secret=SECRET, redirect_uri=REDIRECT_URI,
                                              scope=SCOPE)
    return spotipy.Spotify(auth_manager=client_credentials_manager)


# The main function of the script.
# Initiates a Spotity connection, and saves a new playlist with the reteived Apple Music tracks.
def main():
    remove_error_log_file()
    am_playlist_data = load_playlist_data()
    my_sp_user = sp_auth()
    create_playlist(am_playlist_data, my_sp_user)


# The script is executed
if __name__ == '__main__':
    main()
