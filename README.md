Setup and Installation
Clone or download this repository to your local machine.

In the project root directory, create a .env file to securely store your TMDB credentials:

Code snippet
TMDB_API_TOKEN=your_actual_tmdb_bearer_token_here
Ensure your main.py is in the same directory as your .env file.

Usage
Run the script from your terminal:

Bash
python main.py
Prompt Options:
Minimum Rating: Input a value between 0 and 10.

Year Range: Examples:

2020> (Year 2020 and newer)

<2015 (Year 2015 and older)

2010-2020 (Custom range between 2010 and 2020 inclusive)

Leave blank for any year.

Language Code: Input a 2-letter ISO code (e.g., en for English, ja for Japanese, es for Spanish) or leave blank.

Number of Movies: Select how many movies you want to review.

Code Overview
display_poster_in_terminal(): Fetches the poster image from TMDB, resizes it appropriately maintaining aspect ratio, and outputs blocks (▀) with foreground and background 24-bit ANSI colors to represent rows of pixels efficiently.

movie_list(): Iterates over the top-rated movie endpoint pages to gather a larger selection pool.

print_movie_info(): Outputs movie details including titles, overviews, ratings, and a clickable TMDB URL alongside the visual poster.
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("README.md written successfully.")
