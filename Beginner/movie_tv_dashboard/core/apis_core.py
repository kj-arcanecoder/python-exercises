import logging
import os
import time
from dotenv import load_dotenv
import requests

logger = logging.getLogger(__name__)

base_url = "https://api.themoviedb.org/3/"
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

def get_trending(media_type):
    """Forms the URL for trending, and calls the API.

    Args:
        media_type (str): type of media (movie or TV)

    Returns:
        list: collection of trending movies or shows
    """
    trending_url = f"{base_url}trending/{media_type}/day"
    return get_api_response(trending_url, "results")

def search(media_type, search_text):
    """Forms the URL for search, and calls the API.

    Args:
        media_type (str): type of media (movie or TV)
        search_text (str): the text user asked to search

    Returns:
        list: collection of searched movies or shows
    """
    search_url = base_url + f"search/{media_type}?query={search_text}"
    return get_api_response(search_url, "results")
    
def get_genre(media_type):
    """Forms the URL for genres list, and calls the API.

    Args:
         media_type (str): type of media (movie or TV)

    Returns:
        list: collection of genres for movies or shows
    """
    genre_url = base_url + f"genre/{media_type}/list"
    return get_api_response(genre_url, "genres")

def get_content_by_genres(media_type, genre_id, page_num):
    """Forms the URL for a genre details, and calls the API.

    Args:
        media_type (str): type of media (movie or TV)
        genre_id (_type_): genre identifier for the API
        page_num (_type_): current page number

    Returns:
        list: collection of movie or shows for a genre for a page.
    """
    genre_data_url = base_url + f"discover/{media_type}?with_genres={genre_id}&page={page_num}"
    return get_api_response(genre_data_url, "results")

def get_total_pages_for_genre(media_type, genre_id):
    """Forms the URL for a genre details, and calls the API.

    Args:
        media_type (str): type of media (movie or TV)
        genre_id (_type_): genre identifier for the API

    Returns:
        str: total number of pages for a genre
    """
    pages_data_url = base_url + f"discover/{media_type}?with_genres={genre_id}"
    return get_api_response(pages_data_url, "total_pages")

def get_total_results_count(media_type, genre_id):
    """Forms the URL for a genre details, and calls the API.

    Args:
        media_type (str): type of media (movie or TV)
        genre_id (_type_): genre identifier for the API

    Returns:
        str: total number of results for a genre
    """
    pages_data_url = base_url + f"discover/{media_type}?with_genres={genre_id}"
    return get_api_response(pages_data_url, "total_results")

def get_top_10(media_type):
    """Forms the URL to get top 10 highest rated movies, and calles the API.

    Args:
        media_type (str): type of media (movie or TV)

    Returns:
        list: collection of top 10 highest rated movies.
    """
    top_movies_url = base_url + f"discover/{media_type}?sort_by=vote_average.desc&vote_count.gte=10000"
    return get_api_response(top_movies_url, "results")

def get_api_response(url, json_tag_name):
    """Generic function to call various APIs of TMDB.

    Args:
        url (str): the URL of TMDB to call
        json_tag_name (str): the tag name from the response to fetch.

    Returns:
        list: collection of response received from the API
    """
    headers = {"Accept": "application/json"}
    try:
        r = get_with_retry(url, headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(
            f"HTTP error: url={url} "
            f"status={e.response.status_code} "
            f"reason={e.response.reason}"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: url={url} error={e}")
    else:
        logger.info(
            f"URL={url} responseCode={r.status_code} "
            f"elapsedTime={r.elapsed.total_seconds()}s status={r.reason}"
        )
        return r.json().get(json_tag_name, [])
    return []
    
def get_with_retry(url, headers, retries=3, backoff=2):
    """Generic function to call API, has a retry mechanism if the 
    API call fails due to SSL error.

    Args:
        url (str): the URL of TMDB to call
        headers (str): API request headers
        retries (int, optional): Max retry call to API. Defaults to 3.
        backoff (int, optional): backoff time before retry. Defaults to 2.

    Returns:
        _type_: _description_
    """
    params = {"api_key": api_key}
    for attempt in range(retries):
        try:
            return requests.get(url, headers=headers, timeout=10, params=params)
        except requests.exceptions.SSLError as e:
            attempts_left = retries - (attempt + 1)
            logger.error(f"SSL error: url={url}, "
                         f"retrying API {attempts_left} attempts left")
            if attempt == retries - 1:
                raise
            time.sleep(backoff * (attempt + 1))