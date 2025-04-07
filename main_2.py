import os
import pandas as pd
from supabase import create_client, Client
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configure Supabase and OpenAI credentials
SUPABASE_URL='https://bgyywwqletveirscgzfa.supabase.co'
SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJneXl3d3FsZXR2ZWlyc2NnemZhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAxMzQ4MjMsImV4cCI6MjA0NTcxMDgyM30.ZTUQXQSyTlAY6pb1jrt7oEtKE9xoYnDB9gIHyWTZ5Yk'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def list_data(table_name: str):
    """
    List data from a Supabase database table.
    
    Parameters:
    table_name (str): The name of the Supabase table to retrieve data from.
    
    Returns:
    list: A list of dictionaries representing the rows in the table.
    """
    try:
        # Fetch data from the specified table
        response = supabase.table(table_name).select("*").execute()
        
        # Return the data as a list of dictionaries
        return response.data
    
    except Exception as e:
        print(f"Error: {e}")
        return []
        
# Example usage
data = list_data("user_preferences")
for row in data:
    print(row)