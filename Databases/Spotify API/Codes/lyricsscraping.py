import requests
import csv
import re
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

name = "The_Smiths" 

# Load existing data from CSV with lyrics URLs
input_csv = f'{name}_songs_with_lyrics.csv'
output_csv = f'{name}_songs_with_lyrics_final.csv'

def fetch_lyrics_from_genius(url):
    """
    Function to scrape lyrics from a Genius song URL, with improved formatting.
    """
    try:
        response = requests.get(url, timeout=10)  # Set a timeout to avoid long stalls
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Fetch all divs matching "Lyrics__Container" for lyrics content
        lyrics = "\n".join(
            div.get_text(separator="\n").strip() for div in soup.find_all("div", class_=re.compile(r"Lyrics__Container"))
        )

        # If no lyrics were found, handle it as a 'Lyrics not found' case
        if lyrics.strip():
            # Replace multiple newlines with single newlines for cleaner output
            return re.sub(r'\n+', '\n', lyrics.strip())
        else:
            print(f"Lyrics not found on page: {url}")
            return "Lyrics not found"
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return "Error"
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")
        return "Error"

# Step 3: Read the existing CSV, scrape lyrics, and write to a new CSV with lyrics included
try:
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['lyrics_text']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        print("Fetching lyrics from Genius...")
        for row in tqdm(reader, desc="Tracks Processed", unit="track"):
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
except KeyboardInterrupt:
    print("Process interrupted. Partial results saved.")
