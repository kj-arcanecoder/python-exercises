import csv
from datetime import datetime
import json
import logging
from pathlib import Path
import msvcrt
import os

logger = logging.getLogger(__name__)

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
    
def get_search_data_dict(results_list, media_type, search_text, results_count):
    """Generates search data dictionary to be saved locally.

    Args:
        results_list (list): list of results
        media_type (str): type of media (movie or TV)
        search_text (str): search text entered by user
        results_count (int): count of results

    Returns:
        dict: search data dictionary
    """
    results_dict = {item['id']: item for item in results_list}
    str_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    search_data_dict = {str_time : {
        'timestamp' : str_time,
        'query_type' : f'{media_type}',
        'query' : f'{search_text}',
        'results_count' : f'{results_count}',
    }}
    search_data_dict[str_time]['results'] = results_dict
    return search_data_dict

def save_results_to_json(search_result, media_type):
    """Saves search results to json file.

    Args:
        search_result (list): list of results
        media_type (str): type of media (movie or TV)
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = 'movies_fetched.json' if media_type == 'movie' else 'shows_fetched.json'
    logger.info(f"Saving results to {file_name}")
    json_path = os.path.join(base_dir, '..', 'data', file_name)
    path = Path(json_path)
    if path.exists():
        content = json.loads(path.read_text())
        for key, value in search_result.items():
            content[key] = value

        path.write_text(json.dumps(content, indent=4))
    else:
        content = json.dumps(search_result, indent=4)
        path.write_text(content)
    logger.info(f"Search data saved to {file_name}")
    
def get_search_history(media_type):
    """Gets the search history from json file

    Args:
        media_type (str): type of media (movie or TV)

    Returns:
        _type_: _description_
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = 'movies_fetched.json' if media_type == 'movie' else 'shows_fetched.json'
    logger.info(f"Getting search history from {file_name}")
    json_path = os.path.join(base_dir, '..', 'data', file_name)
    path = Path(json_path)
    if path.exists():
        content = json.loads(path.read_text())
        return content
    else:
        return {}
    
def export_to_csv(media_type):
    """Gets the search history and saves all results in csv file.

    Args:
        media_type (str): type of media (movie or TV)
    """
    current_date_time = datetime.now().strftime("%d%m%Y%H%M%S")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    new_csv_file_name = f"{media_type}_results_"+ current_date_time + ".csv"
    data_path = os.path.join(base_dir, '..', 'data', new_csv_file_name)
    
    title_key = "title" if media_type == "movie" else "name"
    date_key = "release_date" if media_type == "movie" else "first_air_date"
    
    search_history = get_search_history(media_type)
    with open(data_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['id','title','release_date','vote_average','popularity'])
            for details in search_history.values():
                for result in details['results'].values():
                    writer.writerow([
                        result['id'],
                        result[title_key],
                        result[date_key],
                        result['vote_average'],
                        result['popularity']
                    ])
    logger.info(f"Data saved to file {new_csv_file_name}")
    
def get_top_10_list(top_movies, media_type):
    top_movies_dict = {}
    title_key = "title" if media_type == "movie" else "name"
    for item in top_movies[:10]:
        top_movies_dict[item[title_key]] = item['vote_average']
    return top_movies_dict