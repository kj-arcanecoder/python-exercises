from datetime import datetime, date, timedelta
import time

import utils as steps_utils

steps_count = []
dates = []

def init():
    """Initialize steps count and dates
    """
    global steps_count, dates
    steps_utils.load_file(steps_count, dates)

def show_menu():
    """Displays the main menu
    """
    steps_utils.clear_cli()
    steps_utils.print_header("Step Tracker")
    print("\n1. Add steps")
    print("\n2. See full progress")
    print("\n3. See weekly progress")
    print("\n4. Exit")
    

def main():
    """The main function, starting point of steps tracker
    """
    init()
    while True:
        show_menu()
        choice = ""
        try:
            choice = int(input("\nEnter input: "))
        except ValueError:
            print("\nInvalid choice, try again")
        else:
            match choice:
                case 1:
                    add_steps()
                case 2:
                    generate_full_stats()
                case 3:
                    generate_weekly_stats()
                case 4:
                    print("\nThank you for using our tracker.")
                    time.sleep(1)
                    break
                case _:
                    print("\nInvalid choice, try again.")
                    time.sleep(1)

def add_steps():
    """Functionality to add steps for a date
    """
    global steps_count, dates
    steps_utils.clear_cli()
    steps_utils.print_header("Step Tracker - Add Steps")
    steps_date_str = input("\nEnter date DD-MM-YYYY (leave blank for today): ")
    today_date = date.today()
    try:
        if not steps_date_str:
            steps_date_obj = today_date
        else:
            steps_date_obj = datetime.strptime(steps_date_str, "%d-%m-%Y").date()
        steps_date_obj = validate_step_date(steps_date_obj, today_date)

    except ValueError as e:
        print(e)
        print("\nReturning to main menu.")
    else:
        step_count = 0
        try:
            step_count = int(input(f"\nEnter the step count on {steps_date_obj}: "))
        except ValueError:
            print("\nInvalid input, returning to main menu.")
        else:
            steps_utils.add_steps_and_date(steps_date_obj, step_count, steps_count, dates)
            print("\nData added, returning to main menu.")
    time.sleep(2)

def validate_step_date(steps_date, today_date):
    """Validate the date input from user

    Args:
        steps_date (Date): date when the steps were taken
        today_date (Date): today's date

    Raises:
        ValueError: if steps_date is not an instance of date
        ValueError: if steps_date is in the future
        ValueError: data for the date already exists

    Returns:
        date: steps_date if validation is successful
    """
    if not isinstance(steps_date, date):
        raise ValueError("Internal error: expected a date object.")
    if steps_date > today_date:
        raise ValueError("Date is in the future.")
    if steps_date in dates:
        raise ValueError("Data for this date is already present.")
    return steps_date

def generate_full_stats():
    """Generates plot for all dates
    """
    global steps_count, dates
    steps_utils.clear_cli()
    steps_utils.print_header("Step Tracker - Generate Full Stats")
    if steps_count and dates:
        sorted_dates, sorted_steps = sort_date_and_steps()
        get_plot_type(sorted_dates, sorted_steps)
    else:
        print("\nNo data present at the moment, returning to main menu.")
    time.sleep(2)

def get_plot_type(sorted_dates, sorted_steps):
    """Get which plot type user wants to see

    Args:
        sorted_dates (List(date)): sorted list of dates in ascending order
        sorted_steps (List(int)): list of steps
    """
    choice = ""
    print("\n1. Generate normal graph")
    print("\n2. Generate scatter graph")
    try:
        choice = int(input("\nEnter input: "))
    except ValueError:
        print("\nInvalid input, returning to main menu.")
    else:
        if choice == 1:
            steps_utils.extract_normal_plot(sorted_dates, sorted_steps)
        elif choice == 2:
            steps_utils.extract_scatter_plot(sorted_dates, sorted_steps)
        else:
             print("\nInvalid input.")
        print("\nReturning to main menu.")
    
def generate_weekly_stats():
    """Generates plot for last 7 days
    """
    global steps_count, dates
    steps_utils.clear_cli()
    steps_utils.print_header("Step Tracker - Generate Weekly Stats")
    if steps_count and dates:
        sorted_dates, sorted_steps = sort_date_and_steps_for_week()
        if sorted_dates and sorted_steps:
            get_plot_type(sorted_dates, sorted_steps)
        else:
            print("\nData for last week not present, returning to main menu.")
    else:
        print("\nNo data present at the moment, returning to main menu.")
    time.sleep(2)

def sort_date_and_steps():
    """Sorts both date and steps on the basis of dates

    Returns:
        date: sorted list of dates
        int: sorted list of steps to map the dates
    """
    combined = sorted(zip(dates, steps_count))
    sorted_dates, sorted_steps = zip(*combined)
    sorted_dates = [d.strftime("%d-%m-%Y") for d in sorted_dates]
    return sorted_dates, list(sorted_steps)

def sort_date_and_steps_for_week():
    seven_days_ago = date.today() - timedelta(days=7)
    pairs = [(d, s) for d, s in zip(dates, steps_count) if d > seven_days_ago]
    if not pairs:
        return [], []
    pairs.sort()   # sorts by date
    sorted_dates, sorted_steps = zip(*pairs)
    sorted_dates = [d.strftime("%d-%m-%Y") for d in sorted_dates]
    return sorted_dates, list(sorted_steps)

if __name__ == '__main__':
    main()