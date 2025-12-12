from collections import defaultdict
import json
import logging
import os
import time

logger = logging.getLogger(__name__)
accounts_file_name = "accounts.json"
transactions_file_name = "transactions.json"

def print_and_log_warn_message(message):
    logger.warning(message)
    print(message)
    
def print_and_log_info_message(message):
    logger.info(message)
    print(message)
    
def print_and_log_error_message(message):
    logger.error(message)
    print(message)
    
def get_all_accounts():
    """ Fetching raw json data

    Args:
        file_name (_type_): JSON file from which data should be fetched from

    Returns:
        _type_: Dictionary
    """
    
    logger.info(f"Fetching raw data from {accounts_file_name}")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', accounts_file_name)
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

def save_account(new_account_dict):
    """ Saving data to json

    Args:
        obj (_type_): Data to be saved
        file_name (_type_): Destination file

    Returns:
        _type_: None
    """
    raw_data = defaultdict(list)
    logger.info(f"Fetching data from {accounts_file_name} to save")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', accounts_file_name)
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
    logger.info(f"Saving data to {accounts_file_name}")
    raw_data.update(new_account_dict)
    with open(data_path, "w") as f:
        json.dump(raw_data, f, indent=4)
    logger.info(f"Saved to file {accounts_file_name}")
    
def save_transactions(transaction_dict):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', transactions_file_name)
    raw_data = defaultdict(list)
    logger.info(f"Fetching data from {transactions_file_name} to save")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', transactions_file_name)
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
    logger.info(f"Saving data to {transactions_file_name}")
    raw_data.update(transaction_dict)
    with open(data_path, "w") as f:
        json.dump(raw_data, f, indent=4)
    logger.info(f"Saved to file {transactions_file_name}")