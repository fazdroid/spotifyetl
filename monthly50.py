#(works, but only 50 results in python)
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a0a3d660eee2446eb15535a6b0e2f93a",
                                               client_secret="96702e9f92084ba1b4ff487181e39ed4",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-read-recently-played"))

# get the date for one month ago from today
current_date = datetime.now()
last_month_date = current_date - timedelta(days=30)
last_month_date_str = last_month_date.strftime('%Y-%m-%d')

# get the user's recently played tracks from last month
results = sp.current_user_recently_played(after=last_month_date_str, limit=50)

# print the track information
for item in results['items']:
    track = item['track']
    print(track['name'], '-', track['artists'][0]['name'])
    print('Album:', track['album']['name'])
    print('Time:', item['played_at'])

# gets genre for each artist (track and album genre don't work)
    artist = sp.artist(track['artists'][0]['id'])
    if 'genres' in artist and len(artist['genres']) > 0:
        print('Genre:', artist['genres'][0])
    else:
        print('Artist genre information not available')

    print('\n')
