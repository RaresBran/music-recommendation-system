import os
import pandas as pd
from supabase import create_client, Client
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Supabase connection details
SUPABASE_URL='https://bgyywwqletveirscgzfa.supabase.co'
SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJneXl3d3FsZXR2ZWlyc2NnemZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAxMzQ4MjMsImV4cCI6MjA0NTcxMDgyM30.ZTUQXQSyTlAY6pb1jrt7oEtKE9xoYnDB9gIHyWTZ5Yk'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize the Google embeddings model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def create_embeddings_for_row(row_text):
    """Generate embeddings for the provided text using Google Generative AI Embeddings."""
    embedding = embedding_model.embed_query(row_text)
    return embedding

def populate_songs_table_with_embeddings(csv_path):
    data = pd.read_csv(csv_path, nrows=100).fillna('')  # Read only the first 10 rows and fill missing values with empty strings
    data_dict = data.to_dict(orient='records')  # Convert to list of dictionaries for batch insert

    # Add embeddings to each record
    for record in data_dict:
        # Concatenate all row values to generate a single string for embeddings
        row_text = ' '.join(str(value) for value in record.values())
        
        # Generate embeddings for the concatenated row text
        embedding = create_embeddings_for_row(row_text)
        
        # Add the embedding to the record
        record["embeddings"] = embedding

    # Insert the records with embeddings into the 'songs' table
    response = supabase.table("songs").insert(data_dict).execute()



# Run the function
csv_file_path = "merged_data.csv"  # Path to your CSV file
populate_songs_table_with_embeddings(csv_file_path)

# my_embed = create_embeddings_for_row("0.0594,1921,0.982,James Levine,0.279,831667,0.211,0,4BJqT0PrAfrxzMOxytFOIz,0.878,10,0.665,-20.096,1,Piano Concerto No. 3 in D Minor, Op. 30: III. Finale. Alla breve,4,1921,0.0366,80.954,['classical performance', 'opera', 'orchestral performance'],0.9440555555555556,0.2645777777777778,328057.11111111107,0.1660888888888888,0.4461634344444444,0.2326722222222222,-19.4915,0.0483055555555555,102.657,0.1657722222222222,25.83333333333333,10.0,1.0,18.0")

# # lets query the table with the embeddings
# response = supabase.rpc("match_songs",
#                         {
#                             "query_embedding": my_embed,
#                             "match_threshold": 0.48, 
#                             "match_count": 1, 
#                         }).execute()
# print(response)
