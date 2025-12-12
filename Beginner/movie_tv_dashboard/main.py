import logging
import time
from logs import logging_config

from core import movie_core, movie_utils

logging_config.setup_logging()
logger = logging.getLogger(__name__)

def show_menu():
    """Displays the main menu
    """
    print("1. Fetch trending movies/shows")
    print("2. Search movies/shows")
    print("3. Browse movies/shows by genre")
    print("4. Show visualizations")
    print("5. View saved history")
    print("6. Export results to CSV")
    print("7. Exit")

def main():
    """Starting point of the quiz application
    """
    logger.info("Starting the quiz application.")
    choice = 0
    while choice != 7:
        movie_utils.clear_and_print_header("Movie-TV Dashboard")
        show_menu()
        try:
            choice = int(input("\nEnter input: "))
        except ValueError:
            print("Invalid choice, try again.")
            logger.warning("Invalid choice added in main menu.")
            time.sleep(1)
        else:
            match choice:
                case 1:
                    movie_core.fetch_trending_movies_or_shows()
                case 2:
                    movie_core.search_movies_or_shows()
                case 3:
                    movie_core.browse_movies_or_shows_by_genre()
                case 4:
                    movie_core.show_visualization()
                case 5:
                    movie_core.view_search_history()
                case 6:
                    movie_core.export_to_csv()
                case 7:
                    print("\nThank you for using the app!")
                    time.sleep(1)
                case _:
                    print("Invalid choice, try again.")
                    logger.warning("Invalid choice added in main menu.")
                    time.sleep(1)
        
    logger.info("Exiting the quiz application.")

if __name__ == '__main__':
    main()