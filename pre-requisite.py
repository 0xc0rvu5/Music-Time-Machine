import spotipy, os
from spotipy.oauth2 import SpotifyOAuth


#run file
#read/agree to conditions
#copy https://example.com/?code=copy_this_link_and_paste_into_terminal_to_populate_token.txt_file


#initialize global variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_SECRET')


#create 'token.txt' file
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        redirect_uri='http://example.com',
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path='token.txt'
    )
)

user_id = sp.current_user()['id']