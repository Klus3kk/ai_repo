# Example for Fiona Apple
import requests
import csv

# Replace with your actual Client ID and Client Secret
CLIENT_ID = ''
CLIENT_SECRET = ''

# Obtain access token
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
)
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {'Authorization': f'Bearer {access_token}'}

# Get artist's ID
search_response = requests.get(
    'https://api.spotify.com/v1/search',
    headers=headers,
    params={'q': 'Fiona Apple', 'type': 'artist'} # Change it for your artist
)
artist_id = search_response.json()['artists']['items'][0]['id']

# Get albums
albums_response = requests.get(
    f'https://api.spotify.com/v1/artists/{artist_id}/albums',
    headers=headers,
    params={'include_groups': 'album,single', 'limit': 50}
)
albums = albums_response.json()['items']

# Collect tracks
tracks = []
for album in albums:
    album_id = album['id']
    album_name = album['name']
    release_date = album['release_date']
    tracks_response = requests.get(
        f'https://api.spotify.com/v1/albums/{album_id}/tracks',
        headers=headers,
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
        # Get audio features
        features_response = requests.get(
            f'https://api.spotify.com/v1/audio-features/{track["id"]}',
            headers=headers
        )
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
        tracks.append(track_info)

# Write to CSV
with open('fiona_apple_songs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = tracks[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for track in tracks:
        writer.writerow(track)
