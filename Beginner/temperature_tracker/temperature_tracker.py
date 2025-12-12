import temperature

import time
import utils as temp_utils

def init():
    """Initializes the data fetched from csv file

    Returns:
        Temperature: class containing temperatures and dates
    """
    temps_data = temperature.Temperature()
    temps_data.temps, temps_data.dates = temp_utils.load_temp_data()
    return temps_data

def show_menu():
    """Displays the main menu
    """
    temp_utils.clear_cli()
    temp_utils.print_header("Temperature Tracker")
    print("\n1. Get min temperature")
    print("2. Get max temperature")
    print("3. Get average temperature")
    print("4. Plot temperature")
    print("5. Exit")

def get_min_temp(temps_data):
    """Displays the min temperature

    Args:
        temps_data (Temperature): class containing temperatures and dates
    """
    min_temp = min(temps_data.temps)
    return min_temp
    
def get_max_temp(temps_data):
    """Displays the max temperature

    Args:
        temps_data (Temperature): class containing temperatures and dates
    """
    max_temp = max(temps_data.temps)
    return max_temp
    
def get_avg_temp(temps_data):
    """Displays the avg temperature

    Args:
        temps_data (Temperature): class containing temperatures and dates
    """
    avg_temp = sum(temps_data.temps)/len(temps_data.temps)
    return avg_temp

def plot_temp(temps_data):
    """Plots the temperature data

    Args:
        temps_data (Temperature): class containing temperatures and dates
    """
    temp_utils.plot_temp(temps_data.temps, temps_data.dates)

def main():
    """Starting point of the temperature tracker
    """
    temps_data = init()
    choice = ""
    while True:
        show_menu()
        try:
            choice = int(input("\nEnter input: "))
        except ValueError:
            print("Invalid choice.")
            time.sleep(2)
        else:
            match choice:
                case 1:
                    min_temp = get_min_temp(temps_data)
                    print(f"Minimum temperature is {min_temp}")
                case 2:
                    max_temp = get_max_temp(temps_data)
                    print(f"Maximum temperature is {max_temp}")
                case 3:
                    avg_temp = round(get_avg_temp(temps_data), 2)
                    print(f"Average temperature is {avg_temp}")
                case 4:
                    plot_temp(temps_data)
                case 5:
                    print("Thank you!")
                    time.sleep(1)
                    break
                case _:
                    print("Invalid choice.")
                    time.sleep(2)
        input("Press Enter to continue")
        
if __name__ == '__main__':
    main()