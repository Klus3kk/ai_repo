import requests
import csv
import json
import re
from bs4 import BeautifulSoup
import time

# Load existing data from CSV with lyrics URLs
input_csv = 'Portishead_songs_with_lyrics.csv'  # Path to your original CSV
output_csv = 'Portishead_songs_with_lyrics2.csv'  # Path to save updated CSV with lyrics text

def fetch_lyrics_from_genius(url):
    """
    Function to scrape lyrics from a Genius song URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the script tag with JSON data for lyrics
        script_tag = soup.find('script', string=re.compile(r'window\.__PRELOADED_STATE__'))
        if script_tag:
            json_text_match = re.search(r'window\.__PRELOADED_STATE__ = JSON\.parse\("(.*)"\);', script_tag.string)
            if json_text_match:
                json_text = json_text_match.group(1).encode().decode('unicode_escape')
                
                # Parse JSON
                state = json.loads(json_text)
                
                # Extract lyrics HTML and convert it to plain text
                lyrics_html = state.get('songPage', {}).get('lyricsData', {}).get('body', {}).get('html', '')
                lyrics_soup = BeautifulSoup(lyrics_html, 'html.parser')
                lyrics = lyrics_soup.get_text(separator="\n").strip()
                
                if lyrics:
                    return lyrics
                else:
                    print(f"Lyrics not found on page: {url}")
                    return "Lyrics not found"
            else:
                print(f"JSON state not found in script on page: {url}")
                return "Lyrics not found"
        else:
            print(f"Script with JSON lyrics data not found on page: {url}")
            return "Lyrics not found"
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return "Error"
    except json.JSONDecodeError as e:
        print(f"JSON decode error for {url}: {e}")
        return "JSON Error"

# Step 3: Read the existing CSV, scrape lyrics, and write to a new CSV with lyrics included
with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['lyrics_text']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        lyrics_url = row['lyrics_url']
        if lyrics_url and lyrics_url != "Lyrics not found":
            lyrics = fetch_lyrics_from_genius(lyrics_url)
            row['lyrics_text'] = lyrics
            # Wait a few seconds between requests to be polite to the Genius servers
            time.sleep(1)
        else:
            row['lyrics_text'] = "Lyrics not found"
        
        writer.writerow(row)
        print(f"Processed: {row['track_name']}")

print(f"Lyrics added to {output_csv}")
