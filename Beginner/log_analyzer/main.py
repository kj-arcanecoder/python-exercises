import logging
import time
import logging_config
from core import utils, parser_core

logging_config.setup_logging()
logger = logging.getLogger(__name__)

def show_menu():
    """Displays the main menu
    """
    print("1. Load & Parse Log File")
    print("2. Show Basic Statistics")
    print("3. Generate Charts (line, bar, pie)")
    print("4. Export Stats to CSV")
    print("5. Exit")

def main():
    """Starting point of the log analyzer
    """
    logger.info("Starting the log analyzer application.")
    choice = 0
    while choice != 5:
        utils.clear_and_print_header("Log Analyzer")
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
                    parser_core.load_and_parse_log_file()
                case 2:
                    parser_core.show_basic_stats()
                case 3:
                    parser_core.generate_charts()
                case 4:
                    parser_core.export_to_csv()
                case 5:
                    print("\nThank you for using the app!")
                    time.sleep(1)
                case _:
                    print("Invalid choice, try again.")
                    logger.warning("Invalid choice added in main menu.")
                    time.sleep(1)
        
    logger.info("Exiting the log analyzer application.")

if __name__ == '__main__':
    main()