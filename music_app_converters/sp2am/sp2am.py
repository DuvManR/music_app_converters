from spotipy.oauth2 import SpotifyClientCredentials
import warnings
import spotipy
import json
import sys

# Spotify Constants
CID = '<YOUR-CLIENT-ID>'
SECRET = '<YOUR_API_SECRET>'
SP_OBJ_ARTISTS_KEY = 'artists'
SP_OBJ_TRACKS_KEY = 'tracks'
SP_OBJ_TRACK_KEY = 'track'
SP_OBJ_ITEMS_KEY = 'items'
SP_OBJ_NAME_KEY = 'name'
SP_PLAYLIST = 'playlist'
SP_ALBUM = 'album'
NEXT_KEY = 'next'

# Output Constants
AM_PLAYLIST_NAME = 'am_playlist_name'
TRACKS = 'tracks'

# Ignore warning messages
warnings.filterwarnings("ignore")



# Extracts a Spotify playlist/track according to a given Spotify url link
def extract_media(my_sp_user):
    # Extracts media id from the given url link
    sp_obj_link = [word for word in sys.argv if word.startswith("https://")][0]
    sp_obj_id = sp_obj_link.split("/")[-1].split("?")[0]

    
    # Extracts data about the requested Spotify object (name & track info)
    if SP_PLAYLIST in sp_obj_link:
        sp_playlist_root = my_sp_user.playlist(sp_obj_id)
        am_future_playlist_name = sp_playlist_root[SP_OBJ_NAME_KEY]
        sp_playlist = sp_playlist_root[SP_OBJ_TRACKS_KEY]
        sp_tracks_lst = sp_playlist[SP_OBJ_ITEMS_KEY]
        while sp_playlist[NEXT_KEY]:  # 100 Songs Buffer
            sp_playlist = my_sp_user.next(sp_playlist)
            sp_tracks_lst.extend(sp_playlist[SP_OBJ_ITEMS_KEY])
    elif SP_ALBUM in sp_obj_link:
        sp_album = my_sp_user.album(sp_obj_id)
        am_future_playlist_name = sp_album[SP_OBJ_NAME_KEY]
        sp_tracks_lst = [{SP_OBJ_TRACK_KEY: track} for track in sp_album[SP_OBJ_TRACKS_KEY][SP_OBJ_ITEMS_KEY]]
    else:
        sp_track = my_sp_user.track(sp_obj_id)
        am_future_playlist_name = sp_track[SP_OBJ_NAME_KEY]
        sp_tracks_lst = [{SP_OBJ_TRACK_KEY: sp_track}]

    # Iterates over the relevant tracks, and for each one saves a string consisted of its name & artists
    tracks_lst = []
    for sp_track in sp_tracks_lst:
        current_track = sp_track[SP_OBJ_TRACK_KEY]
        track_name = current_track[SP_OBJ_NAME_KEY] + ' '
        track_artists = ' '.join([artist[SP_OBJ_NAME_KEY] for artist in current_track[SP_OBJ_ARTISTS_KEY]])
        tracks_lst += [track_name + track_artists]
        
    # Prints the output of the relevant tracks, to be search in Apple Itunes Store
    print(json.dumps({AM_PLAYLIST_NAME: am_future_playlist_name, TRACKS: tracks_lst}))
    
    
# Initiates a Spotify connection
def sp_auth():
    client_credentials_manager = SpotifyClientCredentials(client_id=CID, client_secret=SECRET)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# The main function of the script.
# First, initates a Spotity connection. Then, extracts the relevant data according to the given Spotify link.
def main():
    my_sp_user = sp_auth()
    extract_media(my_sp_user)


# The script is executed    
if __name__ == '__main__':
    main()

