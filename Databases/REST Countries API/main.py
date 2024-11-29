import requests
import pandas as pd
from tqdm import tqdm

# REST Countries API with Region Filtering
base_url = "https://restcountries.com/v3.1/region/"
regions = ["Africa", "Americas", "Asia", "Europe", "Oceania"]

# Function to fetch data for a single region
def fetch_data_by_region(region):
    url = f"{base_url}{region}"
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {region}: {response.status_code}, {response.reason}")
        return []

# Process and Save Data
try:
    all_data = []
    for region in tqdm(regions, desc="Fetching Data by Region"):
        region_data = fetch_data_by_region(region)
        all_data.extend(region_data)

    # Extract Population and Area Data
    rows_population = []
    for country in tqdm(all_data, desc="Processing Country Data"):
        rows_population.append({
            'name': country['name']['common'],
            'population': country.get('population', None),
            'area_km2': country.get('area', None),
            'population_density': (country.get('population', 0) / country.get('area', 1)) if country.get('area') else None
        })

    # Save to CSV
    df_population_area = pd.DataFrame(rows_population)
    df_population_area.to_csv('rest_countries_population_area.csv', index=False)
    print("Population and Area Data Saved!")

    # Extract Languages and Regions
    rows_languages = []
    for country in tqdm(all_data, desc="Processing Languages and Regions"):
        rows_languages.append({
            'name': country['name']['common'],
            'region': country.get('region', None),
            'subregion': country.get('subregion', None),
            'languages': ', '.join(country.get('languages', {}).values())
        })

    # Save to CSV
    df_languages_regions = pd.DataFrame(rows_languages)
    df_languages_regions.to_csv('rest_countries_languages_regions.csv', index=False)
    print("Languages and Regions Data Saved!")

    # Extract Economic Indicators
    rows_economic = []
    for country in tqdm(all_data, desc="Processing Economic Indicators"):
        currencies = ', '.join([currency['name'] for currency in country.get('currencies', {}).values()])
        rows_economic.append({
            'name': country['name']['common'],
            'currency': currencies,
            'timezones': ', '.join(country.get('timezones', []))
        })

    # Save to CSV
    df_economic_indicators = pd.DataFrame(rows_economic)
    df_economic_indicators.to_csv('rest_countries_economic_indicators.csv', index=False)
    print("Economic Indicators Data Saved!")

except Exception as e:
    print(f"Error: {e}")
