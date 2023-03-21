#removing numerical data (dont care about danceability etc)
#works!

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id='a0a3d660eee2446eb15535a6b0e2f93a', client_secret='96702e9f92084ba1b4ff487181e39ed4')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


#Fetch Tracks and Artists
#The next step is data querying. Note that we can only fetch information about 50 or less tracks at a time

artist_name = []
track_name = []
track_popularity = []
artist_id = []
track_id = []
for i in range(0,1000,50):
    track_results = sp.search(q='year:2022', type='track', limit=50,offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        artist_id.append(t['artists'][0]['id'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        track_popularity.append(t['popularity'])


#Put the queried data into the Pandas Dataframe

import pandas as pd
track_df = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_id' : track_id, 'track_popularity' : track_popularity, 'artist_id' : artist_id})
print(track_df.shape)
track_df.head()


#Let’s add information about artists who perform each of the 1000 tracks

artist_popularity = []
artist_genres = []
artist_followers = []
for a_id in track_df.artist_id:
  artist = sp.artist(a_id)
  artist_popularity.append(artist['popularity'])
  artist_genres.append(artist['genres'])
  artist_followers.append(artist['followers']['total'])


#Now add it to the track_df data frame

track_df = track_df.assign(artist_popularity=artist_popularity, artist_genres=artist_genres, artist_followers=artist_followers)
track_df.head()


#The final step before data exploration and visualisation is column types’ inference. This is done manually:

track_df['artist_name'] = track_df['artist_name'].astype("string")
track_df['track_name'] = track_df['track_name'].astype("string")
track_df['track_id'] = track_df['track_id'].astype("string")
track_df['artist_id'] = track_df['artist_id'].astype("string")
print(track_df.info())




#ANALYSIS
#Let’s see how many genres there are in the track_df data frame:

def to_1D(series):
 return pd.Series([x for _list in series for x in _list])
to_1D(track_df['artist_genres']).value_counts().head(20)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize = (14,4))
ax.bar(to_1D(track_df['artist_genres']).value_counts().index[:10],
        to_1D(track_df['artist_genres']).value_counts().values[:10])
ax.set_ylabel("Frequency", size = 12)
ax.set_title("Top genres", size = 14)

print(track_df.sort_values(by=['track_popularity'], ascending=False)[['track_name', 'artist_name']].head(10))



plt.savefig("my_plot.png")
plt.show()
