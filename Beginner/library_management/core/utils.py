from collections import defaultdict
from datetime import datetime
import json
import logging
import os
import time

logger = logging.getLogger(__name__)

def print_and_log_warn_message(message):
    logger.warning(message)
    print(message)
    
def print_and_log_info_message(message):
    logger.info(message)
    print(message)
    
def print_and_log_error_message(message):
    logger.error(message)
    print(message)
    
def get_all_books():
    """ Fetching raw books data

    Returns:
        _type_: Dictionary
    """
    books_filename = 'books.json'
    return get_raw_data(books_filename)
    
def get_all_members():
    """ Fetching raw members json data

    Returns:
        _type_: Dictionary
    """
    members_filename = 'members.json'
    return get_raw_data(members_filename)

def get_raw_data(file_name):
    """ Fetching raw json data

    Args:
        file_name (_type_): JSON file from which data should be fetched from

    Returns:
        _type_: Dictionary
    """
    logger.info(f"Fetching raw data from {file_name}")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', file_name)
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
    
def save_book(book):
    save_raw_data(book, 'books.json')
    
def save_member(new_member):
    save_raw_data(new_member, 'members.json')
    
def save_raw_data(obj, file_name):
    """ Saving data to json

    Args:
        obj (_type_): Data to be saved
        file_name (_type_): Destination file

    Returns:
        _type_: None
    """
    raw_data = defaultdict(list)
    logger.info(f"Fetching data from {file_name} to save")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', file_name)
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
    logger.info(f"Saving data to {file_name}")
    raw_data.update(obj)
    with open(data_path, "w") as f:
        json.dump(raw_data, f, indent=4)
    print_and_log_info_message(f"Saved to file {file_name}")
        
def save_transaction(member_id, book_name, status):
    """ Saving all borrowed or return transactions

    Args:
        member_id (_type_): member ID
        book_name (_type_): book name

    Returns:
        _type_: None
    """
    current_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    transaction_key = member_id + "_" + str(current_date_time) 
    transaction = {transaction_key:{
        "transaction_time" : current_date_time,
        "member_id" : member_id,
        "book_name" : book_name,
        "status" : status
    }}
    transactions_data = defaultdict(list)
    file_name = 'transactions.json'
    logger.info(f"Fetching transactions data from {file_name} to save")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data', file_name)
    try:
        with open(data_path, "r") as f:
            transactions_data = json.load(f)
    except FileNotFoundError:
        print_and_log_error_message("File not found")
        time.sleep(2)
        return {}
    except json.JSONDecodeError:
        print_and_log_error_message("File empty or corrupted, starting fresh.")
        time.sleep(2)
        transactions_data = {}
    logger.info(f"Saving transaction to {file_name}")
    transactions_data.update(transaction)
    with open(data_path, "w") as f:
        json.dump(transactions_data, f, indent=4)
    logger.info(f"Transaction saved to file {file_name}")
    