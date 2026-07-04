r"""
cd C:\Users\melvi\Downloads\VS_Code\Python\Movie_Recommendation
git add .
git commit -m ""
git push
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")

url = "https://api.themoviedb.org/3/movie/top_rated"

'''Set up request parameters'''

headers = {
    "Authorization" : f"Bearer {TMDB_API_TOKEN}",
    "accept" : "application/json"
}
params = {
    "language" : "en-US",
    "page" : 1
}

min_rating = int(input("Enter the minimum rating (0-10): "))
year_release = input("Enter the year of release (YYYY) or leave blank for any year: ")
language = input("Enter the language code (e.g., 'en' for English) or leave blank for any language: ")

request = requests.get(url, headers=headers, params=params)

if request.status_code == 200:
    data = request.json()
    movies = data["results"]

    # Filters

    filtered_movies = [movie for movie in movies if movie["vote_average"] >= min_rating]
    # Year of release
    if year_release:
        filtered_movies = [movie for movie in filtered_movies if movie["release_date"].startswith(year_release)]


    if filtered_movies:
        print(f"Movies with a rating of {min_rating} or higher:")
        for movie in filtered_movies:
            print("------------------------------")
            print(f"{movie['title']}")
            print(f"Overview: {movie['overview']}")
            print(f"Release Date: {movie['release_date']}")
            print(f"Language: {movie['original_language']}")
            print(f"Rating: {movie['vote_average']}")
    else:
        print(f"No movies found")

    print("------------------------------")

    # When printing, don't just give filter but also additional information

# Potential Features
# 1. Give URL link to the movie
# 2. Display images???