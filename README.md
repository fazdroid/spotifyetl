# spotifyetl
Spotify ETL

ETL process based on Spotify API data.
Generate your Spotify API access token here: https://developer.spotify.com/console/get-recently-played/

In the 24 hour folder:
We are going to build a simple data pipeline (or in other words, a data feed) that downloads Spotify data on what songs we've listened to in the last 24 hours, and saves that data in a SQLite database.

We will schedule this pipeline to run daily. After a few months we will end up with our own, private Spotify played tracks history dataset!

'24hours' - takes the tracks you played within 24 hours


In the monthly folder:
'monthly50' - takes the last 50 tracks you listened to in the past month, starting with the most recent, which prints in Python
'monthly50sql' - takes the last 50 tracks and inputs the data into an SQL database
'monthlypandas' - takes the last 50 tracks and creates visuals using pandas based on genres


