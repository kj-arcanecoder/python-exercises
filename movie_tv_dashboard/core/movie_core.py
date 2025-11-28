from datetime import datetime
import json
import logging
import time
from . import movie_utils, apis_core, plot_core

logger = logging.getLogger(__name__)

def fetch_trending_movies_or_shows():
    """Starting point of trending movies/shows section.
    """
    logger.info("In Fetch trending movies/shows section.")
    movie_utils.clear_and_print_header("Fetch trending movies/shows")
    show_movie_or_tv_menu("Fetch trending")
    while True:
        try:
            menu_choice = int(input("\nEnter choice : "))
        except ValueError:
            print("Invalid choice, try again.")
        else:
            match menu_choice:
                case 1:
                    fetch_trending_movies()
                    break
                case 2:
                    fetch_trending_shows()
                    break
                case _:
                    print("Invalid choice, try again.")
                    
def show_movie_or_tv_menu(menu_type):
    """Generates a generic menu for movie and tv for various sections.

    Args:
        menu_type (str): String to append in the menu before media type.
    """
    print(f"1. {menu_type} Movies")
    print(f"2. {menu_type} Shows")
    
def fetch_trending_movies():
    """Fetches trending movies from the API and displays them in the CLI.
    """
    logger.info("Fetching trending movies")
    trending_movies_list = apis_core.get_trending("movie")
    if trending_movies_list:
        logger.info(f"Results fetched from API successfully.")
        display_movies_or_shows(trending_movies_list, "movie")
        movie_utils.pause()
    else:
        print("\nUnable to fetch movies data right now, try again after sometime.")
        time.sleep(2)
        
def fetch_trending_shows():
    """Fetches trending shows from the API and displays them in the CLI.
    """
    logger.info("Fetching trending shows")
    trending_shows_list = apis_core.get_trending("tv")
    if trending_shows_list:
        logger.info(f"Results fetched from API successfully.")
        display_movies_or_shows(trending_shows_list, "tv")
        movie_utils.pause()
    else:
        print("\nUnable to fetch shows data right now, try again after sometime.")
        time.sleep(2)
        
def search_movies_or_shows():
    """Starting point of Search movies/shows section.
    """
    logger.info("In Search movies/shows section.")
    movie_utils.clear_and_print_header("Search movies/shows")
    show_movie_or_tv_menu("Search")
    while True:
        try:
            menu_choice = int(input("\nEnter choice : "))
        except ValueError:
            print("Invalid choice, try again.")
        else:
            match menu_choice:
                case 1:
                    search_movies()
                    break
                case 2:
                    search_shows()
                    break
                case _:
                    print("Invalid choice, try again.")

def search_movies():
    """Logic to handle movie search scenario, display the data and save locally.
    """
    media_type = "movie"
    search_text = input("\nEnter the movie that you want to search : ")
    logger.info(f"Searching movie {search_text}")
    movies_result = apis_core.search(media_type, search_text)
    if movies_result:
        results_count = len(movies_result)
        logger.info(f"Results fetched from API successfully.")
        display_movies_or_shows(movies_result, media_type)
        save_search_history(media_type, search_text, movies_result, results_count)
        movie_utils.pause()
    else:
        print("\nUnable to fetch movies data right now, try again after sometime.")
        time.sleep(2)
    
def search_shows():
    """Logic to handle shows  search scenario, display the data and save locally.
    """
    media_type = "tv"
    search_text = input("\nEnter the show that you want to search : ")
    logger.info(f"Searching show {search_text}")
    shows_result = apis_core.search(media_type, search_text)
    if shows_result:
        results_count = len(shows_result)
        logger.info(f"Results fetched from API successfully.")
        display_movies_or_shows(shows_result, media_type)
        save_search_history(media_type, search_text, shows_result, results_count)
        movie_utils.pause()
    else:
        print("\nUnable to fetch shows data right now, try again after sometime.")
        time.sleep(2)

def save_search_history(media_type, search_text, results, results_count):
    """Saves the search history data in local.

    Args:
        media_type (str): type of media (movie or TV)
        search_text (str): the text user entered for search
        results (list): search results received from the API
        results_count (int): count of results
    """
    logger.info(f"Saving {media_type} search results to file.")
    search_dict_data = movie_utils.get_search_data_dict(results, media_type, search_text, results_count)
    movie_utils.save_results_to_json(search_dict_data, media_type)
        
def browse_movies_or_shows_by_genre():
    """Starting point of Browse by Genre section.
    """
    logger.info("In Browse by Genre section.")
    movie_utils.clear_and_print_header("Browse by Genre")
    show_movie_or_tv_menu("Get genre for")
    while True:
        try:
            menu_choice = int(input("\nEnter choice : "))
        except ValueError:
            print("Invalid choice, try again.")
        else:
            match menu_choice:
                case 1:
                    get_genre("movie")
                    break
                case 2:
                    get_genre("tv")
                    break
                case _:
                    print("Invalid choice, try again.")
                    
def get_genre(media_type):
    """Fetches and displays the genres list, asks user for input
    to fetch which genre data.

    Args:
        media_type (_type_): _description_
    """
    print("\nLoading genres, please wait...")
    genre_list = apis_core.get_genre(media_type)
    if genre_list:
        display_genres(media_type, genre_list)
        while True:
            try:
                menu_choice = int(input("\nEnter choice : ")) - 1
            except ValueError:
                print("Invalid choice, try again.")
            else:
                if 0 <= menu_choice < len(genre_list):
                    genre_id = genre_list[menu_choice]['id']
                    genre_name = genre_list[menu_choice]['name']
                    page_num = 1
                    logger.info("Getting the total number of pages")
                    total_pages = apis_core.get_total_pages_for_genre(media_type, genre_id)
                    total_pages = int(total_pages) if total_pages else None
                    get_genre_page_data(media_type, genre_id, genre_name, page_num, total_pages)
                        
                break
    else:
        print("\nUnable to get information right now.")
        movie_utils.pause()

def get_genre_page_data(media_type, genre_id, genre_name, page_num, total_pages):
    """Gets page wise data for a genra which user selected, and displays the same. 
    User can navigate to different pages as well to see more details.

    Args:
        media_type (str): type of media (movie or TV)
        genre_id (str): genre id for reference in the API
        genre_name (str): name of genre
        page_num (int): current page number
        total_pages (int): max number of pages
    """
    print(f"\nLoading data for {genre_name}, please wait...")
    while True and total_pages:
        logger.info(f"Total pages for {genre_name} = {total_pages}")
        movie_utils.clear_and_print_header(f"Browse by {genre_name} Genre")
        print("Loading, please wait...")
        content_by_genres = apis_core.get_content_by_genres(media_type, genre_id, page_num)
        if content_by_genres:
            movie_utils.clear_and_print_header(f"Browse by {genre_name} Genre")
            display_movies_or_shows(content_by_genres, media_type)
            print(f"\nPage {page_num} of {total_pages}")
            if page_num > 1:
                msg = ("\nPress 1 to go to next page, "
                                "press 2 to go to previous page or press 9 to exit: ")
            else:
                msg = ("\nPress 1 to go to next page "
                                "or press 9 to exit: ")
            continue_browsing = int(input(msg))
            match continue_browsing:
                case 1:
                    page_num += 1
                case 2:
                    page_num -= 1
                case 9:
                    break
                case _:
                    print("Invalid choice, returning to main menu.")
                    time.sleep(2)
                    break
        else:
            print("Unable to fetch content right now, try again after sometime.")
            movie_utils.pause()
            break

def display_genres(media_type, genre_list):
    """Displays all the genres fetched from the API in the CLI.

    Args:
        media_type (str): type of media (movie or TV)
        genre_list (list): collection of genres
    """
    logger.info(f"Displaying genres for {media_type}")
    for i in range(len(genre_list)):
        if i % 2 == 0:
            print(f"{i+1}. {genre_list[i]['name']}".ljust(60), end="")
        else:
            print(f"{i+1}. {genre_list[i]['name']}")

def display_movies_or_shows(media_list, media_type):
    """Generic function to display movies or shows details for various sections.

    Args:
        media_list (list): collection of movies or shows
        media_type (str): type of media (movie or TV)
    """
    logger.info(f"Displaying {media_type} information")
    print(f"\n{'Title':<80} {'Rating':<10}"
          f"{'Popularity':<10} {'Release Date':<15}"
          f"{'Vote Count':<10}\n")
    title_key = "title" if media_type == "movie" else "name"
    date_key = "release_date" if media_type == "movie" else "first_air_date"
    for item in media_list:
        title = item.get(title_key, "N/A")
        raw_date = item.get(date_key, "")
        try:
            release_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            release_date = "Unknown"
        vote_average = round(float(item.get("vote_average", 0)), 1)
        rating = f"{vote_average}/10"
        popularity = round(float(item.get("popularity", 0)), 1)
        vote_count = item.get("vote_count", 0)
        print(f"{title:<80} {rating:<10}"
              f"{popularity:<10} {release_date:<15}"
              f"{vote_count:<10}")
        
def view_search_history():
    """Starting point of view search history section. 
    """
    logger.info("In view search history section.")
    movie_utils.clear_and_print_header("Search History")
    show_movie_or_tv_menu("Search history for")
    while True:
        try:
            menu_choice = int(input("\nEnter choice : "))
        except ValueError:
            print("Invalid choice, try again.")
        else:
            match menu_choice:
                case 1:
                    get_search_history("movie")
                    break
                case 2:
                    get_search_history("tv")
                    break
                case _:
                    print("Invalid choice, try again.")
    
def show_saved_history_menu():
    """Menu for search history section
    """
    print("1. View movie search history")
    print("2. View TV search history")
    
def get_search_history(media_type):
    """Gets the search history from the file and displays in CLI.

    Args:
       media_type (str): type of media (movie or TV)
    """
    movie_utils.clear_and_print_header("Search History")
    logger.info("Fetching search history from saved file.")
    search_history = movie_utils.get_search_history(media_type)
    if search_history:
        title_key = "title" if media_type == "movie" else "name"
        logger.info("Search history data found, printing the results.")
        print(f"\n{'Timestamp':<20} {'Query Type':<15}"
          f"{'Query text':<30} {'Results Count':<20} {'Top 3 Results':<20}\n")
        for timestamp, search_data in search_history.items():
            top_3 = []
            top_3 = str([r[title_key] for r in list(search_data['results'].values())[:3]])
            print(f"{timestamp:<20} {search_data['query_type'].title():<15}"
                  f"{search_data['query']:<30} {search_data['results_count']:<20}"
                  f"{top_3:<20}")
        movie_utils.pause()
    else:
        logger.info("No search history found.")
        print("\nNo search history found, returning to main menu.")
        time.sleep(2)

def export_to_csv():
    """Exports saved search history data to a CSV file.
    """
    logger.info("In export to CSV section.")
    movie_utils.clear_and_print_header("Search History")
    show_movie_or_tv_menu("Export")
    while True:
        try:
            menu_choice = int(input("\nEnter choice : "))
        except ValueError:
            print("Invalid choice, try again.")
        else:
            match menu_choice:
                case 1:
                    movie_utils.export_to_csv("movie")
                    break
                case 2:
                    movie_utils.export_to_csv("tv")
                    break
                case _:
                    print("Invalid choice, try again.")
    time.sleep(1)
    print("CSV exported successfully with your seach history,"
          " please find the file in the data folder.")
    print("Returning to main menu.")
    time.sleep(2)
    
def show_visualization():
    """Starting point of show visualization section.
    """
    logger.info("In show visualization section.")
    movie_utils.clear_and_print_header("Show Visualization")
    show_visualization_menu()
    while True:
        try:
            menu_choice = int(input("\nEnter choice : "))
        except ValueError:
            print("Invalid choice, try again.")
        else:
            match menu_choice:
                case 1:
                    plot_top_media_type()
                    break
                case 2:
                    plot_genre_distribution()
                    break
                case _:
                    print("Invalid choice, try again.")
    
def show_visualization_menu():
    """Displays the visualization menu in the CLI.
    """
    print("1. Line Chart of Top 10 by Rating")
    print("2. Pie Chart of Genre Distribution")
    
def plot_top_media_type():
    """Fetches the top 10 data from the API, generates and saves the plot 
    for the same.
    """
    media_type = ""
    movie_utils.clear_and_print_header("Line Chart of Top 10")
    show_movie_or_tv_menu("Line Chart of Top 10")
    while True:
        try:
            menu_choice = int(input("\nEnter choice : "))
        except ValueError:
            print("Invalid choice, try again.")
        else:
            match menu_choice:
                case 1:
                    media_type = "movie"
                    break
                case 2:
                    media_type = "tv"
                    break
                case _:
                    print("Invalid choice, try again.")
    logger.info(f"Getting top 10 {media_type}s.")
    print(f"Getting top 10 {media_type}s, please wait...")
    top_10 = apis_core.get_top_10(media_type)
    if top_10:
        top_10_dict = movie_utils.get_top_10_list(top_10, media_type)
        plot_core.plot_top_10(top_10_dict, media_type)
        print("\nReturning to main menu.")
    else:
        logger.info("Unable to get top movies.")
        print("\nUnable to get top movies, returning to main menu.")
    time.sleep(2)

def plot_genre_distribution():
    """Fetches all genres from the API, the fetches counts for all genres one 
    by one and then saves and generates a pie plot.
    """
    media_type = ""
    movie_utils.clear_and_print_header("Pie Chart of Genre Distribution")
    show_movie_or_tv_menu("Genre Distribution of")
    while True:
        try:
            menu_choice = int(input("\nEnter choice : "))
        except ValueError:
            print("Invalid choice, try again.")
        else:
            match menu_choice:
                case 1:
                    media_type = "movie"
                    break
                case 2:
                    media_type = "tv"
                    break
                case _:
                    print("Invalid choice, try again.")
    print("\nFetching info for all genres, this will take some time.")
    logger.info("Getting all genres.")
    print(f"Getting all genres and its data, please wait...")
    genre_list = apis_core.get_genre(media_type)
    if genre_list:
        total_genre_results = []
        for genre in genre_list:
            logger.info(f"Getting total count for {genre['name']}")
            genre_results = apis_core.get_total_results_count(media_type, genre['id'])
            if not genre_results:
                logger.info("Unable to get genre distribution.")
                print("\nUnable to get genre distribution, returning to main menu.")
                time.sleep(2)
                return
            total_genre_results.append(genre_results)
        genre_names = [genre['name'] for genre in genre_list]
        print("Generating the pie chart.")
        plot_core.plot_genre_distribution(genre_names, total_genre_results, media_type)
        print("\nReturning to main menu.")
    else:
        logger.info("Unable to get genre distribution.")
        print("\nUnable to get genre distribution, returning to main menu.")
    time.sleep(2)
