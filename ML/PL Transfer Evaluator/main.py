import time
import logging

from core import app_utils, app_core
import logging_config

logging_config.setup_logging()
logger = logging.getLogger(__name__)

def show_menu():
    """Displays the main menu
    """
    print("1. Show evaluation metrics")
    print("2. Show plots")
    print("3. Predict player's transfer value")
    print("4. Exit")
    
def main():
    """Starting point of the PL Transfer Evaluator application
    """
    logger.info("Starting the PL Transfer Evaluator application.")
    app_core.init_all_ml_models()
    while True:
        app_utils.clear_and_print_header("PL Transfer Evaluator")
        show_menu()
        try:
            choice = int(input("\nEnter input: "))
        except ValueError:
            print("Invalid choice, return to main menu.")
            logger.warning("Invalid choice added in main menu.")
        else:
            match choice:
                case 1:
                    app_core.display_ml_metrics()
                case 2:
                    app_core.show_plots()
                case 3:
                    app_core.predict_new_player_value()
                case 4:
                    print("\nThank you!")
                    time.sleep(1)
                    break
                    
    logger.info("Exiting the application.")

if __name__ == '__main__':
    main()