import requests
import csv

# Spotify API credentials
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

# Genius API credentials
GENIUS_ACCESS_TOKEN = ''
artist_name = "Portishead"

# Step 1: Obtain Spotify access token
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
)
auth_response_data = auth_response.json()
spotify_access_token = auth_response_data['access_token']
spotify_headers = {'Authorization': f'Bearer {spotify_access_token}'}

# Step 2: Get Spotify artist's ID
search_response = requests.get(
    'https://api.spotify.com/v1/search',
    headers=spotify_headers,
    params={'q': artist_name, 'type': 'artist'}
)
search_data = search_response.json()
if not search_data['artists']['items']:
    print(f"No artist found for '{artist_name}'")
    exit()
artist_id = search_data['artists']['items'][0]['id']

# Step 3: Genius API function to fetch lyrics URL
def get_lyrics_url(track_name, artist_name):
    genius_url = "https://api.genius.com/search"
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
    params = {'q': f"{track_name} {artist_name}"}
    response = requests.get(genius_url, headers=headers, params=params)
    
    if response.status_code == 200:
        results = response.json()['response']['hits']
        for hit in results:
            if hit['result']['primary_artist']['name'].lower() == artist_name.lower():
                return hit['result']['url']
    return None

# Step 4: Get albums for the artist
albums_response = requests.get(
    f'https://api.spotify.com/v1/artists/{artist_id}/albums',
    headers=spotify_headers,
    params={'include_groups': 'album,single', 'limit': 50}
)
albums = albums_response.json()['items']

# Step 5: Collect track info and lyrics URL
tracks = []
for album in albums:
    album_id = album['id']
    album_name = album['name']
    release_date = album['release_date']
    
    # Get tracks in the album
    tracks_response = requests.get(
        f'https://api.spotify.com/v1/albums/{album_id}/tracks',
        headers=spotify_headers,
        params={'limit': 50}
    )
    album_tracks = tracks_response.json()['items']
    
    for track in album_tracks:
        track_info = {
            'track_name': track['name'],
            'album_name': album_name,
            'release_date': release_date,
            'track_id': track['id'],
            'duration_ms': track['duration_ms']
        }
        
        # Get Spotify audio features
        features_response = requests.get(
            f'https://api.spotify.com/v1/audio-features/{track["id"]}',
            headers=spotify_headers
        )
        if features_response.status_code == 200:
            features = features_response.json()
            track_info.update({
                'danceability': features.get('danceability'),
                'energy': features.get('energy'),
                'key': features.get('key'),
                'loudness': features.get('loudness'),
                'mode': features.get('mode'),
                'speechiness': features.get('speechiness'),
                'acousticness': features.get('acousticness'),
                'instrumentalness': features.get('instrumentalness'),
                'liveness': features.get('liveness'),
                'valence': features.get('valence'),
                'tempo': features.get('tempo')
            })
        
        # Get Genius lyrics URL
        lyrics_url = get_lyrics_url(track['name'], artist_name)
        track_info['lyrics_url'] = lyrics_url if lyrics_url else "Lyrics not found"
        
        tracks.append(track_info)

# Step 6: Write data to CSV file
csv_filename = f'{artist_name}_songs_with_lyrics.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = tracks[0].keys() if tracks else []
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for track in tracks:
        writer.writerow(track)

print(f"Data for {artist_name} has been saved to {csv_filename}")
