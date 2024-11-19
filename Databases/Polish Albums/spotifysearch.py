import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import logging
from unidecode import unidecode
from spotipy.exceptions import SpotifyException
import os

# Configure logging
logging.basicConfig(filename='polish_artists.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='',
    client_secret=''
), requests_timeout=10)

# Read the list of Polish artists
with open('polish_artists.txt', 'r', encoding='utf-8') as file:
    polish_artists = [line.strip() for line in file.readlines()]

# Check progress
if os.path.exists('polish_albums.csv'):
    existing_data = pd.read_csv('polish_albums.csv', encoding='utf-8')
    processed_artists = set(existing_data['Artist'].unique())
else:
    processed_artists = set()

# Function to handle retries for API requests
def retry_request(func, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return func()
        except SpotifyException as e:
            if e.http_status == 429:  # Rate limit error
                retry_after = int(e.headers.get("Retry-After", delay))
                print(f"Rate limited. Retrying after {retry_after} seconds.")
                time.sleep(retry_after)
            else:
                print(f"Spotify API error: {e}")
                logging.error(f"Spotify API error: {e}")
                time.sleep(delay)
        except Exception as e:
            print(f"Error during request: {e}")
            logging.error(f"Error during request: {e}")
            time.sleep(delay)
    raise Exception("Failed after several retries")

# Fetch album data
for i, artist_name in enumerate(polish_artists):
    if artist_name in processed_artists:
        print(f"Skipping already processed artist: {artist_name}")
        continue

    print(f"{i + 1}: {artist_name} [{(i + 1) / len(polish_artists) * 100:.2f}%]")
    logging.info(f"Fetching data for artist: {artist_name}")

    artist_albums = []
    try:
        # Normalize artist name
        normalized_artist_name = unidecode(artist_name)

        # Search for artist
        results = retry_request(lambda: sp.search(q='artist:' + normalized_artist_name, type='artist'))
        if results['artists']['items']:
            artist_id = results['artists']['items'][0]['id']

            # Fetch all albums with pagination
            albums = []
            offset = 0
            max_pages = 100  # Safety limit to avoid infinite loops
            current_page = 0

            while True:
                response = retry_request(
                    lambda: sp.artist_albums(artist_id, album_type='album', country='PL', limit=50, offset=offset)
                )
                albums.extend(response['items'])
                print(f"Fetched {len(albums)} albums so far (Page {current_page + 1})...")

                if not response.get('next') or current_page >= max_pages:
                    print("No more pages to fetch or reached the maximum number of pages.")
                    break

                offset += 50
                current_page += 1

            # Process album details
            for album in albums:
                album_details = retry_request(lambda: sp.album(album['id']))
                genres = album_details['genres'] if album_details['genres'] else sp.artist(artist_id)['genres']
                artist_albums.append({
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
            print(f"Artist not found: {artist_name}")
            logging.warning(f"Artist not found: {artist_name}")
    except Exception as e:
        print(f"Error while fetching data for {artist_name}: {e}")
        logging.error(f"Error for {artist_name}: {e}")
    time.sleep(1)

    # Save progress to CSV after processing the artist
    if artist_albums:
        df_artist = pd.DataFrame(artist_albums)
        if os.path.exists('polish_albums.csv'):
            df_artist.to_csv('polish_albums.csv', mode='a', index=False, header=False, encoding='utf-8')
        else:
            df_artist.to_csv('polish_albums.csv', index=False, encoding='utf-8')

    print(f"Saved albums for {artist_name}")
    logging.info(f"Saved albums for {artist_name}")

print("All data saved to polish_albums.csv")
logging.info("All data saved to polish_albums.csv")
