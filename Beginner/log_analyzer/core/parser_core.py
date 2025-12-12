import logging
import time
from . import utils, stats_core, charts_core

logger = logging.getLogger(__name__)

def load_and_parse_log_file():
    """Loads and parses the sample log file, and saves the parsed logs 
    to a new json file.
    """
    logger.info("Starting point of load and parse log file.")
    utils.clear_and_print_header("Load & Parse Log File")
    print("\nEnsure that sample log file is placed in the data folder "
    "with name 'sample_logs' and extension .log or .txt.")
    utils.pause()
    
    logs_dict = utils.generate_parsed_logs()
    if logs_dict:
        parsed_json_file_name = utils.generate_parsed_logs_json(logs_dict)
        print(f"Logs parsed succesfully, the file can be found in data/{parsed_json_file_name}")
        print("\nReturning to main menu.")
    else:
        print("\nNo logs data found to parse, returning to main menu.")
    time.sleep(3)
    logger.info("End of load and parse log file.")
    
def show_basic_stats():
    """Starting point of show basic stats section, displays the menu 
    and takes input from user.
    """
    logger.info("Starting point of show basic stats.")
    utils.clear_and_print_header("Show Basic Stats")
    parsed_logs = utils.get_parsed_logs_data()
    if parsed_logs:
        show_basic_stats_menu()
        try:
            choice = int(input("\nEnter input: "))
        except ValueError:
            print("\nInvalid choice, try again.")
            logger.warning("Invalid choice, returning to main menu.")
            time.sleep(2)
        else:
            match choice:
                case 1:
                    top_10_ips(parsed_logs)
                case 2:
                    count_by_http(parsed_logs)
                case 3:
                    count_by_http_status(parsed_logs)
                case 4:
                    most_requested_urls(parsed_logs)
                case 5:
                    print("\nReturning to main menu.")
                    time.sleep(2)
                case _:
                    print("\nInvalid choice, returning to main menu.")
                    time.sleep(2)
    else:
        print("\nNo parsed logs found, returning to main menu.")
        time.sleep(2)
    
def show_basic_stats_menu():
    """Displays the basic stats menu
    """
    print("1. Top 10 most frequent IP addresses")
    print("2. Request count by HTTP method (GET/POST/DELETE…)")
    print("3. Count of each HTTP status code (200, 404, 500, etc.)")
    print("4. Most requested URLs")
    print("5. Return to main menu")
    
def top_10_ips(parsed_logs):
    """Finds the top 10 ip addresses and displays the same.

    Args:
        parsed_logs (dict): dictionary of parsed logs 
    """
    stats_core.top_10_ips(parsed_logs)
    utils.pause()


def count_by_http(parsed_logs):
    """Calculates the counts of each http methods and displays the same

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    stats_core.count_by_http(parsed_logs)
    utils.pause()

def count_by_http_status(parsed_logs):
    """Calculates the counts of each http statuses and displays the same

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    stats_core.count_by_http_status(parsed_logs)
    utils.pause()

def most_requested_urls(parsed_logs):
    """Calculates the counts ofall urls and displays the top ones

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    stats_core.most_requested_urls(parsed_logs)
    utils.pause()

def generate_charts():
    """Starting point of generate charts menu, displays the menu 
    and takes input from user.
    """
    logger.info("Starting point of generate charts.")
    utils.clear_and_print_header("Generate charts")
    parsed_logs = utils.get_parsed_logs_data()
    if parsed_logs:
        show_generate_charts_menu()
        try:
            choice = int(input("\nEnter input: "))
        except ValueError:
            print("\nInvalid choice, try again.")
            logger.warning("Invalid choice, returning to main menu.")
            time.sleep(2)
        else:
            match choice:
                case 1:
                    plot_traffic_per_hour(parsed_logs)
                case 2:
                    plot_top_10_urls(parsed_logs)
                case 3:
                    plot_http_status_distribution(parsed_logs)
                case _:
                    print("\nInvalid choice, returning to main menu.")
                    time.sleep(2)
    else:
        print("\nNo parsed logs found, returning to main menu.")
        time.sleep(2)

def show_generate_charts_menu():
    """Displays the generate charts menu
    """
    print("1. Line chart – Traffic per hour")
    print("2. Bar chart – Top 10 URLs")
    print("3. Pie chart – HTTP status distribution")
    
def plot_traffic_per_hour(parsed_logs):
    """Plots a line graph for number of requests per hour.

    Args:
        parsed_logs (dict): dictionary of parsed logs 
    """
    
    hour_timestamp = stats_core.traffic_per_hour(parsed_logs)
            
    logger.info("Plotting traffic per hour")
    charts_core.plot_traffic_per_hour(hour_timestamp)
    
    print("\nPlot generated and saved successfully, returning to main menu.")
    time.sleep(2)
    
def plot_top_10_urls(parsed_logs):
    """Plots a bar chart for the top 10 requested urls 

    Args:
        parsed_logs (dict): dictionary of parsed logs 
    """
    urls = stats_core.top_10_requested_urls(parsed_logs)
    
    logger.info("Plotting top 10 urls")
    charts_core.plot_top_urls(urls)
    
    print("\nPlot generated and saved successfully, returning to main menu.")
    time.sleep(2)

def plot_http_status_distribution(parsed_logs):
    """Plots a pie chart for the HTTP status distribution

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    http_statuses = stats_core.http_status_distribution(parsed_logs)
    
    logger.info("Plotting HTTP Status distribution")
    charts_core.plot_http_status_distribution(http_statuses)
    
    print("\nPlot generated and saved successfully, returning to main menu.")
    time.sleep(2)
    
def export_to_csv():
    """Fetches the parsed logs and exports to a CSV file.
    """
    logger.info("Starting point of export to csv.")
    utils.clear_and_print_header("Export to CSV")
    print("Exporting to CSV file, please wait.")
    time.sleep(3)
    parsed_logs = utils.get_parsed_logs_data()
    if parsed_logs:
        utils.export_to_csv(parsed_logs)
        print("Logs exported to CSV file successfully.")
    else:
        print("\nNo parsed logs found, returning to main menu.")
        time.sleep(2)