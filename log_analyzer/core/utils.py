import csv
from datetime import datetime
import json
import logging
import msvcrt
import os
from pathlib import Path
import re


logger = logging.getLogger(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

def clear_and_print_header(heading):
    """Clears CLI and displays the heading of any requested section

    Args:
        heading (str): heding to display
    """
    clear_cli()
    print(f"*************************{heading}*************************\n")
    
def clear_cli():
    """Clears the cli window
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    

def pause(msg="\nPress any key to continue..."):
    """Pauses the program

    Args:
        msg (str, optional): Defaults to "\nPress any key to continue...".
    """
    print(msg)
    msvcrt.getch()
    
def generate_parsed_logs():
    """Finds the sample logs file, parses it and returns a dictionary
    of the logs data.

    Returns:
        dict: dictionary of the logs data.
    """
    logs_dict = {}
    log_ext_path = os.path.join(base_dir, '..', 'data', 'sample_logs.log')
    txt_ext_path = os.path.join(base_dir, '..', 'data', 'sample_logs.txt')
    
    regex = r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<url>\S+) .*" (?P<status>\d{3}) (?P<size>\d+)'
    
    logger.info(f"Looking for sample logs file.")
    path = Path(log_ext_path)
    if not path.exists():
        path = Path(txt_ext_path)
    if path.exists():
        
        parse_logs(logs_dict, regex, path)
    else:
        logger.warning(f"No logs file found.")
    return logs_dict

def parse_logs(logs_dict, regex, path):
    """Reads the log file line by line and parses the data.

    Args:
        logs_dict (dict): dictionary where logs data will be saved
        regex (str): regex used to parse the data
        path (Path): path of the sample logs file
    """
    logger.info(f"Loading the sample logs file.")
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            log = re.search(regex,line)
            if not log:
                continue
            timestamp, ip = log.group('timestamp'), log.group('ip')
            method, url = log.group('method'), log.group('url')
            status, size = log.group('status'), log.group('size')
            logs_dict[timestamp] = {'ip' : ip,
                                                'method' : method,
                                                'url' : url,
                                                'status' : status,
                                                'size' : size}
            
def generate_parsed_logs_json(logs_dict):
    """Saves the parsed logs dictionary to json file.

    Args:
        logs_dict (dict): dictionary of parsed logs data
    """
    timestamp = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    json_file_name = f'parsed_logs_{timestamp}.json'
    logger.info(f"Saving the parsed logs json file {json_file_name}.")
    json_path = os.path.join(base_dir, '..', 'data', json_file_name)
    
    path = Path(json_path)
    content = json.dumps(logs_dict, indent=4)
    path.write_text(content)
    logger.info(f"{json_file_name} saved successfully.")
    
    return json_file_name

def get_parsed_logs_data():
    """Gets the parsed logs data

    Returns:
        dict: dictionary of parsed logs data
    """
    logger.info("Getting the data from parsed logs file.")
    parsed_logs = {}
    parsed_json_file = get_latest_parsed_file()
    if parsed_json_file:
        parsed_file_dir = os.path.join(base_dir, '..', 'data', parsed_json_file)
        path = Path(parsed_file_dir) 
        content = path.read_text()
        parsed_logs = json.loads(content)
    return parsed_logs

def get_latest_parsed_file():
    """Gets the latest parsed file if multiple parsed files exist
    in data folder

    Returns:
        str: parsed json file name
    """
    parsed_json_file = ""
    data_dir = os.path.join(base_dir, '..', 'data')
    data_dir_files = os.listdir(data_dir)
    parsed_json_files = [file for file in data_dir_files if "parsed_logs_" in file]
    if len(parsed_json_files) == 1:
        parsed_json_file = parsed_json_files[0]
    else:
        timestamp = None
        for file in parsed_json_files:
            t = re.search('_([0-9]{14})\.json$',file).group(1)
            t_dt = datetime.strptime(t,'%Y%m%d%H%M%S')
            if not timestamp:
                timestamp = t_dt
                parsed_json_file = file
            elif timestamp < t_dt:
                timestamp = t_dt
                parsed_json_file = file
    logger.info(f"Found parsed file {parsed_json_file}")
    return parsed_json_file

def get_hour_timestamp(timestamp):
    """Gets the hour part from the timestamp

    Args:
        timestamp (str): timestamp string

    Returns:
        str: hour of the timestamp
    """
    hour = re.search(r':(\d{2}):\d{2}:\d{2}', timestamp).group(1)
    return hour

def export_to_csv(parsed_logs):
    """Saves all the parsed logs in csv file.

    Args:
        parsed_logs (dict): dictionary of parsed logs
    """
    current_date_time = datetime.now().strftime("%d%m%Y_%H%M")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    new_csv_file_name = f"exported_stats_"+ current_date_time + ".csv"
    data_path = os.path.join(base_dir, '..', 'data', new_csv_file_name)
    
    with open(data_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['ip','url','status','timestamp','method','size'])
            for timestamp, details in parsed_logs.items():
                writer.writerow([
                    details['ip'],
                    details['url'],
                    details['status'],
                    timestamp,
                    details['method'],
                    details.get('size', '')
                ])
    logger.info(f"Data saved to file {new_csv_file_name}")