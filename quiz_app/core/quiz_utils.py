import json
from pathlib import Path
import logging
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
    
def store_results(player_name, counter, result, correct_perc):
    """Stores the quiz results of a player in the leaderboard file

    Args:
        player_name (string): name of the player
        counter (int): questions attempted
        result (int): correct answers given
        correct_perc (float): questions correctly answered percentage 
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    leaderboard_path = os.path.join(base_dir, '..', 'data', 'quiz_leadboard.json')
    logger.info("Storing results in quiz_leadboard.json")
    path = Path(leaderboard_path)
    if path.exists():
        leaderboard_dict = load_leaderboard(path)
        if leaderboard_dict:
            if player_name in leaderboard_dict.keys():
                counter = int(leaderboard_dict[player_name]['questions_attempted']) + counter
                result = int(leaderboard_dict[player_name]['correct_answers']) + result
                correct_perc = round(float((result/counter)*100), 2)
                add_player_to_dict(player_name, correct_perc, leaderboard_dict, counter, result)
            else:
                leaderboard_dict[player_name] = {}
                add_player_to_dict(player_name, correct_perc, leaderboard_dict, counter, result)
            save_existing_file(path, leaderboard_dict)
            
    else:
        save_new_file(player_name, counter, result, correct_perc, path)

def load_leaderboard(path):
    """loads the existing leader board

    Args:
        path (Path): the path of the leaderboard file

    Returns:
        dict: leader board dictionary
    """
    logger.info("Loading the leaderboard from quiz_leadboard.json")
    content = path.read_text() 
    leaderboard_dict = json.loads(content)
    return leaderboard_dict

def add_player_to_dict(player_name, correct_perc, leaderboard_dict, attempted, answers):
    """Adds the player data to dictionary whether new or existing player.

    Args:
        player_name (string): name of the player
        correct_perc (float): questions correctly answered percentage
        leadboard_dict (dict): existing leader board dictionary
        attempted (int): questions attempted
        answers (int): questions correctly answered
    """
    leaderboard_dict[player_name]['questions_attempted'] = attempted
    leaderboard_dict[player_name]['correct_answers'] = answers
    leaderboard_dict[player_name]['correct_percentage'] = correct_perc

def save_new_file(player_name, counter, result, correct_perc, path):
    """Saves leaderboard data to new file

    Args:
        player_name (string): name of the player
        counter (int): questions attempted
        result (int): questions correctly answered
        correct_perc (float): questions correctly answered percentage
        path (Path): the path of the leaderboard file
    """
    logger.info("Saving the leaderboard for the first time in quiz_leadboard.json")
    player_dict = extract_player_dict(player_name, counter, result, correct_perc)
    content = json.dumps(player_dict, indent=4)
    path.write_text(content)
    
def save_existing_file(path, leaderboard_dict):
    """Saves leaderboard data to an existing file

    Args:
        path (Path): the path of the leaderboard file
        leadboard_dict (dict): existing leader board dictionary
    """
    logger.info("Saving player information in quiz_leadboard.json")
    content = json.dumps(leaderboard_dict, indent=4)
    path.write_text(content)

def extract_player_dict(player_name, counter, result, correct_perc):
    """Creates a dictionary for a new player if no leaderboard exists.

    Args:
        player_name (string): name of the player
        counter (int): questions attempted
        result (int): questions correctly answered
        correct_perc (float): questions correctly answered percentage

    Returns:
        dict: a dictionary with the player data.
    """
    return {player_name : {
            'questions_attempted' : counter,
            'correct_answers' : result,
            'correct_percentage' : correct_perc
        }}
    
def load_leaderboard_to_display():
    """Loads the leaderboard from the file to display on the app.

    Returns:
        dictionary: dictionary of leaderboard data
    """
    logger.info("Fetching the leaderboard from quiz_leadboard.json")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    leaderboard_path = os.path.join(base_dir, '..', 'data', 'quiz_leadboard.json')
    path = Path(leaderboard_path)
    if path.exists():
        leaderboard_dict = load_leaderboard(path)
        if leaderboard_dict:
            sorted_players = dict(sorted(
                leaderboard_dict.items(), 
                key=lambda item: item[1]["correct_answers"], reverse=True))
            top_10_dict = dict(list(sorted_players.items())[:10])
            return top_10_dict
        else:
            return {}
    else:
        return {}