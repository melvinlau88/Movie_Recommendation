r"""
cd C:\Users\melvi\Downloads\VS_Code\Python\Movie_Recommendation
git add .
git commit -m "Fixed image output in terminal"
git push
"""
import os
import requests
from dotenv import load_dotenv
import io
from PIL import Image

def display_poster_in_terminal(poster_snippet, width=50):
    if not poster_snippet:
        print("No poster available.")
        return

    full_poster_url = f"https://image.tmdb.org/t/p/w200{poster_snippet}"

    response = requests.get(full_poster_url, timeout=5)
    if response.status_code != 200:
        print("No poster available")
        return

    img = Image.open(io.BytesIO(response.content))

    aspect_ratio = img.height / img.width
    
    height = int(width * aspect_ratio * 0.5)

    # Ensures height is even for the 2 pixel rows representation
    if height % 2 != 0:
        height += 1

    # Resize image to fit terminal width and make colours to be only RGB
    img = img.resize((width, height)).convert("RGB")

    for i in range(0, height, 2):
        line = ""
        for j in range(width):
            # Two pixel rows are represented accounting for the 2 steps in the loop
            r1, g1, b1 = img.getpixel((j, i))       
            r2, g2, b2 = img.getpixel((j, i + 1))    
            
            line += f"\033[38;2;{r1};{g1};{b1}m\033[48;2;{r2};{g2};{b2}m▀"
        print(line + "\033[0m")

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
year_release = input("Enter Year Range (e.g., '2020> OR 2020-2023 OR <2023'): ")
language = input("Enter the language code (e.g., 'en' for English) or leave blank for any language: ")

request = requests.get(url, headers=headers, params=params)

if request.status_code == 200:
    data = request.json()
    movies = data["results"]

    # Filters

    filtered_movies = [movie for movie in movies if movie["vote_average"] >= min_rating]
    # Year of release
    if year_release:
        if year_release[-1] == ">":
            movie_year = int(year_release[0:4])
            filtered_movies = [movie for movie in filtered_movies if int(movie["release_date"][:4]) >= int(year_release[0:4])]

        elif year_release[0] == "<":
            movie_year = int(year_release[1:5])
            filtered_movies = [movie for movie in filtered_movies if int(movie["release_date"][:4]) <= int(year_release[1:5])]

        elif "-" in year_release:
            first_year, second_year = map(int, year_release.split("-"))
            filtered_movies = [movie for movie in filtered_movies if first_year <= int(movie["release_date"][:4]) <= second_year]

            
    if filtered_movies:
        for movie in filtered_movies:
            print("------------------------------")
            print(f"{movie['title']}")
            print(f"Overview: {movie['overview']}")
            print(f"Release Date: {movie['release_date']}")
            print(f"Language: {movie['original_language']}")
            print(f"Rating: {movie['vote_average']}")

            # Display movie poster
            # Get URL
            poster_path = movie.get("poster_path")

            image_bytes = io.BytesIO(requests.get(f"https://image.tmdb.org/t/p/w500{poster_path}").content)

            # Display poster in terminal
            display_poster_in_terminal(poster_path, width=100)
            
            
            
    else:
        print(f"No movies found")

    print("------------------------------")


    # When printing, don't just give filter but also additional information

# Potential Features
# 1. Give URL link to the movie
# 2. Display images???
# 3. Force a format for the year range input to avoid errors
# 4. Randomize movie