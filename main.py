import os
from random import random
import requests
from dotenv import load_dotenv
import io
from PIL import Image
import random

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
            
            # Print using the 24-bit color escape sequence for foreground and background colors 
            line += f"\033[38;2;{r1};{g1};{b1}m\033[48;2;{r2};{g2};{b2}m▀"
        print(line + "\033[0m")

def print_movie_info(movie):
    print("------------------------------")
    print(f"{movie['title']}")
    print(f"Overview: {movie['overview']}")
    print(f"Release Date: {movie['release_date']}")
    print(f"Language: {movie['original_language']}")
    print(f"Rating: {movie['vote_average']}")
    print(f"Link: https://www.themoviedb.org/movie/{movie['id']}")

    poster_path = movie.get("poster_path")
    image_bytes = io.BytesIO(requests.get(f"https://image.tmdb.org/t/p/w500{poster_path}").content)
    display_poster_in_terminal(poster_path, width=100)

while True:
    min_rating = input("Enter the minimum rating (0-10): ")
    if not min_rating.isdigit() or not (0 <= int(min_rating) <= 10):
        print("Invalid Input. Please enter a number between 0 and 10")
        continue
    else:
        min_rating = int(min_rating)
        
    year_release = input("Enter Year Range (e.g., '2020> OR 2020-2023 OR <2023 or blank for any year'): ")
    if year_release == "":
        year_release = None
    elif year_release and not (year_release[-1] == ">" or year_release[0] == "<" or "-" in year_release):
        print("Invalid Input. Please use 'YYYY>', '<YYYY', or 'YYYY-YYYY'")
        continue

    language = input("Enter the language code (e.g., 'en' for English) or leave blank for any language: ")
    if language and len(language) != 2:
        print("Invalid Input. Please enter a 2-letter language code")
        continue
    num_movies = input("How many movies would you like to review? (1 = Randomise Movie): ")
    if num_movies == "":
        num_movies = 1
    elif not num_movies.isdigit() or int(num_movies) <= 0:
        print("Invalid Input. Please enter a positive whole number")
        continue
    else:
        num_movies = int(num_movies)
    break

def movie_list(url, headers, params, num_movies):
    all_movies = []
    # num_pages = 10

    for page in range(1, 5):
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            break

        data = response.json()
        all_movies.extend(data["results"])

    return all_movies[:num_movies]


load_dotenv()
TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")

url = "https://api.themoviedb.org/3/movie/top_rated"

'''Set up request parameters'''

headers = {
    "Authorization" : f"Bearer {TMDB_API_TOKEN}",
    "accept" : "application/json"
}
params = {
    "language" : "en-US"
}

movies = movie_list(url, headers, params, num_movies)

if movies:
    if min_rating == 0 and not year_release and not language and num_movies == 1:
        while True:
            randomise = input("Randomise movie? y/n: ")
            if randomise not in ("y", "n"):
                print("Enter y or n")
                continue
            elif randomise.lower() == "y":
                movie = random.choice(movies)
                print_movie_info(movie)
                break
            elif randomise.lower() == "n":
                for movie in movies:
                    print_movie_info(movie)
                print("------------------------------")
                break
    else:
        filtered_movies = [movie for movie in movies if movie["vote_average"] >= min_rating]

        # Year of release
        if year_release:
            if year_release[-1] == ">":
                filtered_movies = [movie for movie in filtered_movies if int(movie["release_date"][:4]) >= int(year_release[0:4])]

            elif year_release[0] == "<":
                filtered_movies = [movie for movie in filtered_movies if int(movie["release_date"][:4]) <= int(year_release[1:5])]

            elif "-" in year_release:
                first_year, second_year = map(int, year_release.split("-"))
                filtered_movies = [movie for movie in filtered_movies if first_year <= int(movie["release_date"][:4]) <= second_year]

        # Language
        if language:
            filtered_movies = [movie for movie in filtered_movies if movie["original_language"] == language]

        if filtered_movies:
            for movie in filtered_movies:
                print_movie_info(movie)
        else:
            print("No movies found")

        print("------------------------------")
else:
    print("Could not fetch movies.")
    