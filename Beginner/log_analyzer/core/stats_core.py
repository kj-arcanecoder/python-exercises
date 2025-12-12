import logging
from . import utils

logger = logging.getLogger(__name__)

def top_10_ips(parsed_logs):
    """Finds the top 10 ip addresses and displays the same.

    Args:
        parsed_logs (dict): dictionary of parsed logs 
    """
    ip_details = {}
    for log_detail in parsed_logs.values():
        current_ip = log_detail['ip']
        if current_ip not in ip_details.keys():
            ip_details[current_ip] = 1
        else:
            ip_details[current_ip] += 1
    
    logger.info("Sorting and displaying the top 10 IP addresses.")
    ip_details = dict(sorted(ip_details.items(), key=lambda x: x[1], reverse=True))
    print(f"\n{'IP':<25} {'Count':<15}")
    for i, (ip, count) in enumerate(ip_details.items(), start=1):
        print(f"{ip:<25} {count:<15}")
        if i == 10:
            break
        
def count_by_http(parsed_logs):
    """Calculates the counts of each http methods and displays the same

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    http_details = {}
    for log_detail in parsed_logs.values():
        current_http = log_detail['method']
        if current_http not in http_details.keys():
            http_details[current_http] = 1
        else:
            http_details[current_http] += 1
    logger.info("Sorting and displaying the top HTTP methods.")
    http_details = dict(sorted(http_details.items(), key=lambda x: x[1], reverse=True))
    print(f"\n{'Method':<25} {'Count':<15}")
    for method, count in http_details.items():
        print(f"{method:<25} {count:<15}")

def count_by_http_status(parsed_logs):
    """Calculates the counts of each http statuses and displays the same

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    http_statuses = http_status_distribution(parsed_logs)
    print(f"\n{'HTTP Status':<25} {'Count':<15}")
    for status, count in http_statuses.items():
        print(f"{status:<25} {count:<15}")

def http_status_distribution(parsed_logs):
    """Calculates the counts of each http statuses

    Args:
        parsed_logs (dict): dictionary of parsed logs

    Returns:
        dict: counts of each http statuses
    """
    http_statuses = {}
    for log_detail in parsed_logs.values():
        current_http_status = log_detail['status']
        if current_http_status not in http_statuses.keys():
            http_statuses[current_http_status] = 1
        else:
            http_statuses[current_http_status] += 1
    logger.info("Sorting and displaying the top 10 HTTP statuses.")
    http_statuses = dict(sorted(http_statuses.items(), key=lambda x: x[1], reverse=True))
    return http_statuses

def most_requested_urls(parsed_logs):
    """Calculates the counts ofall urls and displays the top ones

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    urls = {}
    for log_detail in parsed_logs.values():
        current_url = log_detail['url']
        if current_url not in urls.keys():
            urls[current_url] = 1
        else:
            urls[current_url] += 1
    logger.info("Sorting and displaying the top URLs.")
    urls = dict(sorted(urls.items(), key=lambda x: x[1], reverse=True))
    print(f"\n{'URL':<25} {'Count':<15}")
    for status, count in urls.items():
        print(f"{status:<25} {count:<15}")
        
def top_10_requested_urls(parsed_logs):
    """Calculates the counts of all urls and returns the top 10

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    urls = {}
    for log_detail in parsed_logs.values():
        current_url = log_detail['url']
        if current_url not in urls.keys():
            urls[current_url] = 1
        else:
            urls[current_url] += 1
    logger.info("Sorting and returning the top URLs.")
    urls = dict(sorted(urls.items(), key=lambda x: x[1], reverse=True)[:10])
    return urls

def traffic_per_hour(parsed_logs):
    """Generates the stats for the number of requests per hour

    Args:
        parsed_logs (dict): dictionary of parsed logs

    Returns:
        dict: hour wise count of requests 
    """
    logger.info("Calculating requests per hour")
    hour_timestamp = {}
    timestamps = parsed_logs.keys()
    for timestamp in timestamps:
        hour = utils.get_hour_timestamp(timestamp)
        if hour not in hour_timestamp.keys():
            hour_timestamp[hour] = 1
        else:
            hour_timestamp[hour] += 1
    return hour_timestamp