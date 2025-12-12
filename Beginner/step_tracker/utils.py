from datetime import datetime
import json
import matplotlib.pyplot as plt
import os
from pathlib import Path

base_dir = os.path.dirname(os.path.abspath(__file__))
steps_data_file = os.path.join(base_dir, "steps_data.json")

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
    
def save_data(steps_count, dates):
    """Saves the step count and dates to json

    Args:
        steps_count (int): list of step count
        dates (date): list of dates
    """
    path = Path(steps_data_file)
    steps_dict = set_steps_dict(steps_count, dates)
    content = json.dumps(steps_dict, indent=4)
    path.write_text(content)

def add_steps_and_date(steps_date, step_count, steps_count, dates):
    """Adds the new step and date to the respective objects and saves data to file 

    Args:
        steps_date (date): new step date added by user
        step_count (int): new step count added by user
        steps_count (List(int)): full collection of steps count
        dates (List(date)): full collection of steps dates
    """
    steps_count.append(step_count)
    dates.append(steps_date)
    save_data(steps_count, dates)

def extract_normal_plot(sorted_dates, sorted_steps):
    """Generates a standard plot

    Args:
        sorted_dates (List(date)): full collection of steps dates
        sorted_steps (List(int)): full collection of steps count
    """
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots()
    ax.plot(sorted_dates, sorted_steps, linewidth=3)
    ax.set_title("Weekly Steps", fontsize=24)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Steps", fontsize=14)
    ax.tick_params(labelsize=10)
    plt.show()
    
def extract_scatter_plot(sorted_dates, sorted_steps):
    """Generates a scatter plot

    Args:
        sorted_dates (List(date)): full collection of steps dates
        sorted_steps (List(int)): full collection of steps count
    """
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots()
    ax.scatter(sorted_dates, sorted_steps, s=40)
    ax.set_title("Weekly Steps", fontsize=24)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Steps", fontsize=14)
    ax.tick_params(labelsize=10)
    plt.show()

def load_file(steps_count, dates):
    """loads the steps data file during initialize

    Args:
        steps_count (List): empty steps count list
        dates (List): empty dates list
    """
    steps_dict = {}
    path = Path(steps_data_file)
    if path.exists():
        content = path.read_text()
        try:
            steps_dict = json.loads(content)
        except json.JSONDecodeError:
            pass
        if(steps_dict):
            for date, step in steps_dict.items():
                steps_count.append(int(step))
                dates.append(datetime.strptime(date, "%d-%m-%Y").date())
        
def set_steps_dict(steps_count, dates):
    """creates a dictionary of dates and steps to save it to json

    Args:
        steps_count (List): list of steps count data
        dates (List): list of dates

    Returns:
        dict: dictionary of dates and steps
    """
    steps_dict = {}
    for i in range(len(steps_count)):
        steps_dict[dates[i].strftime("%d-%m-%Y")] = steps_count[i]
    return steps_dict