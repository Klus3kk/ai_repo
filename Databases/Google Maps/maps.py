import googlemaps
import pandas as pd
from tqdm import tqdm
import time

# Google Maps API key
API_KEY = ""
gmaps = googlemaps.Client(key=API_KEY)

# List of major cities in Poland
cities = ["Warsaw", "Kraków", "Gdańsk", "Wrocław", "Poznań", "Łódź", "Katowice"]

# Categories to search for
categories = ["restaurant", "museum", "park", "hospital", "school"]

# Function to fetch Points of Interest
def fetch_pois(city, category):
    places = []
    query = f"{category} in {city}, Poland"
    response = gmaps.places(query=query)
    places.extend(response.get("results", []))
    
    # Handle pagination
    while "next_page_token" in response:
        time.sleep(2)
        response = gmaps.places(query=query, page_token=response["next_page_token"])
        places.extend(response.get("results", []))
    return places

# Function to get administrative region and postal code
def get_geocode_info(lat, lng):
    result = gmaps.reverse_geocode((lat, lng))
    if result:
        address_components = result[0].get("address_components", [])
        admin_region = None
        postal_code = None
        for component in address_components:
            if "administrative_area_level_1" in component["types"]:
                admin_region = component["long_name"]
            if "postal_code" in component["types"]:
                postal_code = component["long_name"]
        return admin_region, postal_code
    return None, None

# Collect data
data = []
for city in tqdm(cities, desc="Processing cities"):
    for category in categories:
        pois = fetch_pois(city, category)
        for poi in pois:
            lat = poi["geometry"]["location"]["lat"]
            lng = poi["geometry"]["location"]["lng"]
            admin_region, postal_code = get_geocode_info(lat, lng)
            
            data.append({
                "city": city,
                "category": category,
                "name": poi.get("name"),
                "address": poi.get("formatted_address"),
                "latitude": lat,
                "longitude": lng,
                "rating": poi.get("rating"),
                "user_ratings_total": poi.get("user_ratings_total"),
                "administrative_region": admin_region,
                "postal_code": postal_code,
            })

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv("poland_poi_dataset.csv", index=False)
print("Dataset saved as poland_poi_dataset.csv")
