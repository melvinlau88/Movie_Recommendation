"""
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
