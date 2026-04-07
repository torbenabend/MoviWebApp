"""
Utility module for retrieving movie data from the OMDb API.

This module loads an API key from environment variables and provides
a function to fetch movie metadata such as title, director, release
year, and poster URL. The OMDb API is accessed via HTTP requests using
the requests library.

The API key must be defined in the environment variable ``API_KEY``.
"""
import requests
import os
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES
load_dotenv()
API_KEY = os.getenv("API_KEY")


def fetch_omdb_data(title):
    """
    Fetch movie information from the OMDb API by title.

    Sends an HTTP GET request to the OMDb API and extracts relevant
    metadata for a movie matching the provided title.

    Args:
        title (str): The title of the movie to search for.

    Returns:
        tuple[str, str, int, str]: A tuple containing:
            - Movie title
            - Director name
            - Release year as an integer
            - Poster image URL
        dict: Empty dictionary if no movie is found.

    Raises:
        requests.exceptions.Timeout: If the request exceeds the timeout limit.
        requests.exceptions.RequestException: If a general HTTP request error occurs.
        KeyError: If expected fields are missing in the API response.
        ValueError: If the year cannot be converted to an integer.
    """
    api_url = "https://www.omdbapi.com/"
    query_params = {"apikey": API_KEY, "t": title, "type": "movie"}
    response = requests.get(api_url, params=query_params, timeout=5)
    if response.status_code != requests.codes.ok:
        print("Error:", response.status_code, response.text)
    movie_data = response.json()
    if movie_data["Response"] == "False":
        return {}
    return (
        movie_data["Title"],
        movie_data["Director"],
        int(movie_data["Year"]),
        movie_data["Poster"]
    )
