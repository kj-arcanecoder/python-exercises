from datetime import datetime
import logging
import os
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def plot_top_10(top_movies_dict, media_type):
    """Saves and generates bar plot for the top 10 most rated movies.

    Args:
        top_movies_dict (dict): dictionary of top movies
        media_type (str): type of media (movie or TV)
    """
    movies = top_movies_dict.keys()
    ratings = top_movies_dict.values()
    current_date_time = datetime.now().strftime("%d%m%Y%H%M%S")
    plt.bar(movies, ratings)
    plt.xlabel("Movies")
    plt.ylabel("Ratings")
    plt.title(f"Top 10 Rated {media_type.title()}s")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f'top_10_movies_{current_date_time}.png' if media_type == 'movie' else f'top_10_shows_{current_date_time}.png'
    plot_path = os.path.join(base_dir, '..', 'charts', file_name)
    logger.info(f"Saving top 10 {media_type.title()}s plot")
    plt.savefig(plot_path)
    logger.info(f"Displaying top 10 {media_type.title()}s plot")
    plt.show()

def plot_genre_distribution(genre_names, total_genre_results, media_type):
    """Saves and generates pie plot for the genre distribution per media type.

    Args:
        genre_names (_type_): _description_
        total_genre_results (_type_): _description_
        media_type (_type_): _description_
    """
    current_date_time = datetime.now().strftime("%d%m%Y%H%M%S")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f'genre_distr_movies_{current_date_time}.png' if media_type == 'movie' else f'genre_distr_shows_{current_date_time}.png'
    plot_path = os.path.join(base_dir, '..', 'charts', file_name)
    
    plt.pie(total_genre_results, labels=genre_names, autopct="%1.1f%%")
    plt.title("Genre Distribution")
    plt.savefig(plot_path)
    plt.show()