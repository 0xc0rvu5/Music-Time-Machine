import requests, spotipy, os
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from rich.progress import track


#initialize global variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_SECRET')


#get relevant user input to initiate program functionality.
try:
    os.system('clear')
    print('Welcome to the music time machine. Input the date in which you would like to go back to.')
    year = input('Year:\n ~ ')
    month = format(int(input('Month:\n ~ ')), '02d')
    day = format(int(input('Day:\n ~ ')), '02d')
    date = f'{year}-{month}-{day}'

except KeyboardInterrupt:
    print('\nSee you later.')


#global variables located here because user input is passed into request query.
RESPONSE = requests.get(url=f'https://www.billboard.com/charts/hot-100/{date}/')
SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
TEXT = SOUP.find_all(name='h3', class_='u-letter-spacing-0021')
H3_TEXT = []


def get_songs():
    '''Get the top 100 songs from the specified date, place the songs into H3_TEXT list and print a file called 'Top_100_Songs.txt'.'''
    #exclude list
    sw = 'Songwriter'
    prod = 'Producer'
    imprint = 'Imprint'

    #obtain the text from each h3 header with a class named 'u-letter-spacing-0021' and append it to H3_TEXT list.
    #an exclude list is given due to the lack of specific id/class identifiers for the song names.
    for tag in TEXT:
        text = tag.getText().strip()
        if sw not in text and prod not in text and imprint not in text:
            H3_TEXT.append(text)

    #create a file called 'Top_100_Songs.txt' in 'w' mode. If a new playlist is created the previous file will be overwritten.
    x = 0
    with open('Top_100_Songs.txt', 'w') as f:
        print('Printing file.')
        print(f'Here are the top 100 songs from {year}-{month}-{day}:\n', file=f)
        for el in track(H3_TEXT):
            print(f'{x + 1}: {el}', file=f)
            x += 1
    print('Done')


def get_playlist():
    '''Create a playlist based off of the top 100 songs obtained from get_songs() function and populate playlist into Spotify account.'''
    #authenticate with Spotify and obtain user ID after following pre-requisite in 'pre-requisite.py' file.
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

    #initialize relevant local variables.
    user_id = sp.current_user()['id']
    songs = []

    #obtain each song uri in Spotify then append to songs list. report on any errors.
    print('Creating playlist.')
    for song in track(H3_TEXT):
        result = sp.search(q=f'track:{song} year:{year}', type='track')
        try:
            uri = result['tracks']['items'][0]['uri']
            songs.append(uri)
        except IndexError:
            print(f'Not available: {song}')

    #create a non-public playlist via the songs list obtained and finalize the process.
    playlist = sp.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False)
    sp.playlist_add_items(playlist_id=playlist['id'], items=songs)
    print('Done')


#initiate get_songs() and get_playlist() functions.
try:
    get_songs()
    get_playlist()

except KeyboardInterrupt:
    print('See you later.')