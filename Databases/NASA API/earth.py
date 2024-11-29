import requests
import pandas as pd
from tqdm import tqdm

# NASA API Key
API_KEY = "mLGksc3ThWfPCo8fbfGotDWeZXp11EC3goDoAPtz"

# Example Coordinates and Dates
coordinates = [(37.7749, -122.4194), (34.0522, -118.2437), (40.7128, -74.0060)]  # SF, LA, NY
dates = ["2024-01-01", "2024-01-02", "2024-01-03"]

rows = []

# Loop through coordinates and dates
for lat, lon in tqdm(coordinates, desc="Fetching Data for Coordinates"):
    for date in tqdm(dates, desc=f"Processing Date for Lat {lat}, Lon {lon}", leave=False):
        url = f"https://api.nasa.gov/planetary/earth/assets?lon={lon}&lat={lat}&date={date}&dim=0.1&api_key={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            rows.append({
                'latitude': lat,
                'longitude': lon,
                'date': data.get('date', date),
                'cloud_score': data.get('cloud_score', None),
                'image_url': data.get('url', None)
            })
        else:
            print(f"Failed to fetch data for Lat {lat}, Lon {lon}, Date {date}")

# Save Data to CSV
df_earth_imagery = pd.DataFrame(rows)
df_earth_imagery.to_csv('nasa_earth_imagery_data.csv', index=False)
print("Earth Imagery Data Saved!")
