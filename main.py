import pandas as pd

# Load the two datasets
song_data = pd.read_csv('data.csv')
genre_data = pd.read_csv('data_w_genres.csv')

# Function to extract artists from the list string
def get_artists(artist_str):
    return [x.strip("'[]") for x in artist_str.split(', ')]

# Apply the function to create a new 'artists' column with lists
song_data['artists'] = song_data['artists'].apply(get_artists)

# Explode the 'artists' column to create one row per artist
song_data = song_data.explode('artists')

# Merge the datasets based on the 'artists' column
merged_data = song_data.merge(genre_data, on='artists', how='left')

# Fill any missing genre values with an empty list
merged_data['genres'] = merged_data['genres'].fillna('[]')

# Save the merged dataset to a new CSV file
merged_data.to_csv('merged_data.csv', index=False)