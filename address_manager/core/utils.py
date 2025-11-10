
from collections import defaultdict
import csv
import json
import logging
import os
import time
from datetime import datetime


logger = logging.getLogger(__name__)
contacts_file_name = "contacts.json"

def print_and_log_warn_message(message):
    """Prints a message on cli and logs a warning message

    Args:
        message (str): message to display
    """
    logger.warning(message)
    print(message)
    
def print_and_log_info_message(message):
    """Prints a message on cli and logs an info message

    Args:
        message (str): message to display
    """
    logger.info(message)
    print(message)
    
def print_and_log_error_message(message):
    """Prints a message on cli and logs an error message

    Args:
        message (str): message to display
    """
    logger.error(message)
    print(message)
    
def print_header(heading):
    """Displays the heading of any requested section

    Args:
        heading (str): heding to display
    """
    print(f"*************************{heading}*************************")
    
def clear_cli():
    """Clears the cli window
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def get_all_contacts():
    """Fetches all the contacts present in the file

    Returns:
        dict: Dictionary of all the contacts
    """
    logger.info(f"Fetching contacts data from {contacts_file_name}")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', contacts_file_name)
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print_and_log_error_message("File not found")
        time.sleep(2)
        return {}
    except json.JSONDecodeError:
        print_and_log_error_message("Corrupted file, unable to fetch.")
        time.sleep(2)
        return {}
    
def save_contact(contact_dict):
    """Saves a single contact to file

    Args:
        contact_dict (dict): dictionary of a single contact
    """
    raw_data = defaultdict(list)
    logger.info(f"Fetching data from {contacts_file_name} to save")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', contacts_file_name)
    try:
        with open(data_path, "r") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print_and_log_error_message("File not found")
        time.sleep(2)
        return {}
    except json.JSONDecodeError:
        print_and_log_error_message("Corrupted file, starting fresh.")
        time.sleep(2)
        raw_data = {}
    logger.info(f"Saving data to {contacts_file_name}")
    raw_data.update(contact_dict)
    with open(data_path, "w") as f:
        json.dump(raw_data, f, indent=4)
    logger.info(f"Saved to file {contacts_file_name}")
    
def delete_contact(contact_name):
    """Deletes a single contact from file

    Args:
        contact_name (str): Name of the contact or dict key to be deleted.
    """
    raw_data = defaultdict(list)
    logger.info(f"Fetching data from {contacts_file_name} to save")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', contacts_file_name)
    try:
        with open(data_path, "r") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print_and_log_error_message("File not found")
        time.sleep(2)
        return {}
    except json.JSONDecodeError:
        print_and_log_error_message("Corrupted file, starting fresh.")
        time.sleep(2)
        raw_data = {}
    logger.info(f"Deleting data in {contacts_file_name}")
    raw_data.pop(contact_name)
    with open(data_path, "w") as f:
        json.dump(raw_data, f, indent=4)
    logger.info(f"record deleted in file {contacts_file_name}")
    
def export_to_csv(contacts):
    current_date_time = datetime.now().strftime("%d%m%Y%H%M%S")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    new_csv_file_name = "contacts" + "_" + current_date_time + ".csv"
    data_path = os.path.join(base_dir, '..', 'data', new_csv_file_name)
    try:
        with open(data_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Email", "Address"])
            for name, details in contacts.items():
                writer.writerow([
                    name,
                    details.get("phone", ""),
                    details.get("email", ""),
                    details.get("address", "")
                ])
        print_and_log_info_message(f"CSV file '{new_csv_file_name}' created successfully, saved to path {data_path}.")
    except Exception as e:
        print(f"Error while writing CSV: {e}")