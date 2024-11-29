import requests
import pandas as pd
from tqdm import tqdm

# NASA API KEY
API_KEY = "mLGksc3ThWfPCo8fbfGotDWeZXp11EC3goDoAPtz"
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key={API_KEY}"

# Make the API request
response = requests.get(url)  
if response.status_code == 200:  
    data = response.json()

    # Create DataFrame
    rows = []
    dates = data['near_earth_objects'].keys()
    for date in tqdm(dates, desc="Processing Asteroid Data"):
        for neo in data['near_earth_objects'][date]:
            rows.append({
                'date': date,
                'name': neo['name'],
                'diameter_km': neo['estimated_diameter']['kilometers']['estimated_diameter_max'],
                'velocity_kms': neo['close_approach_data'][0]['relative_velocity']['kilometers_per_second'],
                'closest_approach_au': neo['close_approach_data'][0]['miss_distance']['astronomical'],
                'potentially_hazardous': neo['is_potentially_hazardous_asteroid']
            })

    df_asteroids = pd.DataFrame(rows)
    df_asteroids.to_csv('nasa_asteroid_data.csv', index=False)
    print("Asteroid Data Saved!")
else:
    print(f"Failed to fetch data: {response.status_code}, {response.reason}")
