#(sql database, only 50 results)
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
import sqlite3

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a0a3d660eee2446eb15535a6b0e2f93a",
                                               client_secret="96702e9f92084ba1b4ff487181e39ed4",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-read-recently-played"))

# Set up SQLite database
conn = sqlite3.connect('spotify_tracks.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tracks
             (name text, artist text, album text, played_at text, genre text, PRIMARY KEY (played_at))''')

# get the date for one month ago from today
current_date = datetime.now()
last_month_date = current_date - timedelta(days=30)

# Use Spotify API to retrieve recently played tracks and store them in the database
while last_month_date <= current_date:
    last_month_date_str = last_month_date.strftime('%Y-%m-%d')
    results = sp.current_user_recently_played(after=last_month_date_str, limit=50)

    for item in results['items']:

        track = item['track']
        played_at = item['played_at']
        name = track['name']
        artist = track['artists'][0]['name']
        album = track['album']['name']

        # Get the genre information for the artist
        artist_id = track['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        if 'genres' in artist_info and len(artist_info['genres']) > 0:
            genre = artist_info['genres'][0].title()
        else:
            genre = 'Artist genre information not available'





        # Check if track is already in database and skip if it is
        c.execute("SELECT * FROM tracks WHERE played_at = ?", (played_at,))
        if c.fetchone() is not None:
            continue

        # Insert new track into database
        c.execute("INSERT INTO tracks VALUES (?, ?, ?, ?, ?)", (name, artist, album, played_at, genre))
        conn.commit()

    # Move to the previous day
    last_month_date += timedelta(days=1)

# Print out all the tracks in the database
c.execute("SELECT * FROM tracks")
#for row in c.fetchall():
#    print(row)

# Close database connection
conn.close()
