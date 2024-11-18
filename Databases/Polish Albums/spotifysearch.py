import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
from unidecode import unidecode

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='',
    client_secret=''
))

with open('polish_artists.txt', 'r', encoding='utf-8') as file:
    polish_artists = [line.strip() for line in file.readlines()]

albums_data = []

for i, artist_name in enumerate(polish_artists):
    print(f"{i + 1}: {artist_name} [{(i + 1) / len(polish_artists) * 100:.2f}%]")
    try:
        normalized_artist_name = unidecode(artist_name)
        results = sp.search(q='artist:' + normalized_artist_name, type='artist')
        if results['artists']['items']:
            artist_id = results['artists']['items'][0]['id']
            albums = sp.artist_albums(artist_id, album_type='album', country='PL', limit=50)
            for album in albums['items']:
                album_details = sp.album(album['id'])
                genres = album_details['genres'] if album_details['genres'] else sp.artist(artist_id)['genres']
                albums_data.append({
                    'Album Name': album['name'],
                    'Artist': artist_name,
                    'Year': album['release_date'][:4],  
                    'Release Date': album['release_date'],  
                    'Release Precision': album_details['release_date_precision'],  
                    'Genres': ', '.join(genres),
                    'Tracks': album['total_tracks'],
                    'Album Type': album_details['album_type'],  
                    'Popularity': album_details['popularity'],  
                    'Language': 'Polish'  
                })
        else:
            print(f"Nie znaleziono artysty: {artist_name}")
    except Exception as e:
        print(f"Błąd podczas pobierania danych dla {artist_name}: {e}")
    time.sleep(2) 

df = pd.DataFrame(albums_data)
df.to_csv('polish_albums.csv', index=False, encoding='utf-8')

print("Dane o albumach zapisane w polish_albums.csv")
