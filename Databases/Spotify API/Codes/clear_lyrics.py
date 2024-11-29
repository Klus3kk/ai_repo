import pandas as pd
import re

name = "The_Smiths" # Write spaces with underline

# Load your data into a DataFrame (replace with your actual CSV file path)
data = pd.read_csv(f'{name}_songs.csv')

# Define a function to clean the lyrics_text field
def clean_lyrics(text):
    if pd.isna(text):  # Handle missing lyrics
        return text
    # Use regex to remove section headers like [Chorus], [Verse 1], etc.
    cleaned_text = re.sub(r'\[.*?\]', '', text)
    return cleaned_text.strip()

# Apply the cleaning function to the lyrics_text column
data['lyrics_text'] = data['lyrics_text'].apply(clean_lyrics)

# Save the cleaned data back to a CSV file (optional)
data.to_csv(f'{name}_songs_cleaned.csv', index=False)

# Print a sample to verify
print(data[['track_name', 'lyrics_text']].head())
