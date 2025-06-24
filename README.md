# Music Recommendation System

A modern music discovery platform that leverages machine learning and serverless technologies to generate personalized song recommendations.

## Technology Stack

- **Nuxt 3 & Vue 3** – Front‑end framework for building the web interface
- **TypeScript** – Type safety across the app
- **Tailwind CSS** – Utility‑first styling
- **Supabase** – Authentication and Postgres database with RPC functions
- **LangChain & Google Generative AI** – Embeddings for similarity search
- **Python** – Data preparation and batch import scripts

## Features

- User registration and login backed by Supabase Auth
- Profile setup with favorite genres, artists and release years
- Music matching interface powered by Spotify embeds
- Like/Dislike actions and ability to mark songs as favorites
- Recommendations based on embeddings generated from user preferences and song features
- Stored procedures for fast similarity search in the database
- Dataset preprocessing scripts for merging metadata and generating embeddings

## Results

The system loads over 170k tracks, enriches them with genre information and stores them in Supabase. Embeddings are created using Google's `text-embedding-004` model to enable high quality recommendations. Users receive Spotify links for the top matches based on their likes and favorites.
