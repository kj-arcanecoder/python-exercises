import csv
from datetime import datetime
import os
from pathlib import Path
import sys
from matplotlib import pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))
temp_data_file = os.path.join(base_dir, "daily_temps.csv")

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
    
def load_temp_data():
    """Loads the temperature data from csv file

    Args:
        temps (List): full collection of temperatures
        dates (List): full collection of dates

    Returns:
        List: full collection of temperatures and dates
    """
    path = Path(temp_data_file)
    temps, dates = [], []
    try:
        with path.open() as f:
            reader = csv.DictReader(f, fieldnames=['date', 'temp'])
            for row in reader:
                temps.append(int(row['temp']))
                dates.append(datetime.strptime(row['date'], "%Y-%m-%d").date())
        return temps, dates
    except FileNotFoundError:
        print("No file found, exiting.")
        sys.exit()
        
def plot_temp(temps, dates):
    """Generates a standard plot

    Args:
        temps (List): full collection of temperatures
        dates (List): full collection of dates
    """
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots()
    max_temp, max_date = get_max_temp(temps, dates)
    ax.plot(dates, temps, linewidth=3)
    ax.set_title("Daily Temperature Trend", fontsize=24)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Temperature", fontsize=14)
    ax.scatter(max_date, max_temp, color='red', s=30)
    ax.tick_params(labelsize=10)
    plt.show()
    
def get_max_temp(temps, dates):
    max_temp = temps[0]
    max_date = dates[0]
    for i in range(len(temps)):
        if temps[i] > max_temp:
            max_temp = temps[i]
            max_date = dates[i]
    return max_temp, max_date