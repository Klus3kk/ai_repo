import requests
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point

# Define Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"

# Updated Query for Historic Monuments and Attractions in Poland
query = """
[out:json][timeout:1800];
area["name"="Poland"]->.searchArea;
(
  node["historic"](area.searchArea);
  way["historic"](area.searchArea);
  relation["historic"](area.searchArea);
  node["tourism"](area.searchArea);
  way["tourism"](area.searchArea);
  relation["tourism"](area.searchArea);
  node["amenity"](area.searchArea);
  way["amenity"](area.searchArea);
  relation["amenity"](area.searchArea);
  node["building"](area.searchArea);
  way["building"](area.searchArea);
  relation["building"](area.searchArea);
  node["leisure"](area.searchArea);
  way["leisure"](area.searchArea);
  relation["leisure"](area.searchArea);
);
out center tags;
>;
out skel qt;
"""


# Send the request
response = requests.get(overpass_url, params={"data": query})

# Check if the request was successful
if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit()

# Parse the response
data = response.json()
elements = data.get("elements", [])

# Extract attributes
monuments = []
for elem in elements:
    tags = elem.get("tags", {})
    lat = elem.get("lat") or elem.get("center", {}).get("lat")
    lon = elem.get("lon") or elem.get("center", {}).get("lon")
    if tags.get("name") and lat and lon:
        monuments.append({
            "name": tags.get("name", "Unnamed"),
            "historic": tags.get("historic", "Unknown"),
            "tourism": tags.get("tourism", "Unknown"),
            "description": tags.get("description", "No description available"),
            "latitude": lat,
            "longitude": lon
        })

df = pd.DataFrame(monuments)
df = df.drop_duplicates(subset=["name", "latitude", "longitude"])

print(df.head())

df.to_csv("poland_monuments.csv", index=False)
print(f"\nTotal Monuments Retrieved: {len(df)}")
