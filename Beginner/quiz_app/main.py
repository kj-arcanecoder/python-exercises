import logging
import time

import logging_config
from core import quiz_core, quiz_utils

logging_config.setup_logging()
logger = logging.getLogger(__name__)

def show_menu():
    """Displays the main menu
    """
    print("1. Start Default Quiz (Random Difficulty and Categories)")
    print("2. Start Custom Quiz (Choose Difficulty and Category)")
    print("3. Leaderboard")
    print("4. Exit")
    
def input_player_name():
    """Asks for the name of the player and returns it

    Returns:
        string: player name
    """
    quiz_utils.clear_and_print_header("Trivia Quiz App")
    player_name = input("Enter player name : ").title()
    print(f"\nWelcome {player_name}!")
    time.sleep(2)
    return player_name

def main():
    """Starting point of the quiz application
    """
    logger.info("Starting the quiz application.")
    player_name = input_player_name()
    choice = 0
    while choice != 4:
        quiz_utils.clear_and_print_header("Trivia Quiz App")
        show_menu()
        try:
            choice = int(input("\nEnter input: "))
        except ValueError:
            print("Invalid choice, return to main menu.")
            logger.warning("Invalid choice added in main menu.")
        else:
            match choice:
                case 1:
                    quiz_core.start_default_quiz(player_name)
                case 2:
                    quiz_core.start_custom_quiz(player_name)
                case 3:
                    quiz_core.show_leaderboard()
                case 4:
                    print("\nThank you for playing!")
                    time.sleep(1)

if __name__ == '__main__':
    main()