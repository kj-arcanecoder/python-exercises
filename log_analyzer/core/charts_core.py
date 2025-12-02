from datetime import datetime
import logging
import os
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

def plot_traffic_per_hour(hour_timestamp):
    """Plots the line graph of traffic per hour

    Args:
        hour_timestamp (dict): dictionary of hour and the count of requests per hour
    """
    logger.info(f"Generating the hourly traffic plot")
    fig, ax = plt.subplots()
    ax.plot(hour_timestamp.keys(), hour_timestamp.values(), linewidth=3)
    ax.set_title("Traffic Per Hour", fontsize=24)
    ax.set_xlabel("Hour", fontsize=14)
    ax.set_ylabel("Number of requests", fontsize=14)
    
    timestamp = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    plot_file_name = f'hourly_traffic_{timestamp}.png'
    logger.info(f"Saving the plot {plot_file_name}.")
    plot_path = os.path.join(base_dir, '..', 'charts', plot_file_name)
    plt.savefig(plot_path)
    plt.show()
    
def plot_top_urls(urls):
    """Plots the bar chart of top 10 URLs

    Args:
        urls (dict): dictionary of counts of requests on each URL
    """
    logger.info(f"Generating the top urls plot")
    plt.bar(urls.keys(), urls.values())
    plt.title("Top URLs", fontsize=24)
    plt.xlabel("URLs", fontsize=14)
    plt.ylabel("Number of requests", fontsize=14)
    
    timestamp = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    plot_file_name = f'top_urls_{timestamp}.png'
    logger.info(f"Saving the plot {plot_file_name}.")
    plot_path = os.path.join(base_dir, '..', 'charts', plot_file_name)
    plt.savefig(plot_path)
    plt.show()
    
def plot_http_status_distribution(http_statuses):
    logger.info(f"Generating the top HTTP status plot")
    plt.pie(http_statuses.values(), labels=http_statuses.keys(), autopct="%1.1f%%")
    plt.title("HTTP status distribution", fontsize=24)
    plt.xlabel("HTTP status", fontsize=14)
    plt.ylabel("Number of requests", fontsize=14)
    
    timestamp = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    plot_file_name = f'status_codes_{timestamp}.png'
    logger.info(f"Saving the plot {plot_file_name}.")
    plot_path = os.path.join(base_dir, '..', 'charts', plot_file_name)
    plt.savefig(plot_path)
    plt.show()