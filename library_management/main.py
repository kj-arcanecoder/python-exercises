import logging
import os
import time
import core.utils as lib_utils
import core.library as library
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def show_menu():
    """ Display the main menu. 
    """
    os.system("cls")
    print("================= Library Management =================\n")
    print("1. Add Book")
    print("2. Add Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View All Books")
    print("6. View Members")
    print("7. Exit")
    print("=======================================================")

def main():
    """ The main class to start the library management

    Raises:
        ValueError: When invalid inputs are provided
    """
    logger.info("Application started.")
    lib = library.Library()
    choice = 0
    while choice != 7:
        show_menu()
        try:
            choice = int(input("\nEnter input: "))
        except(ValueError):
            lib_utils.print_and_log_warn_message("Invalid character, try again.")
            time.sleep(2)
            continue
        match choice:
            case 1:
                lib.add_book()
            case 2:
                lib.add_member()
            case 3:
                lib.borrow_book()
            case 4:
                lib.return_book()
            case 5:
                lib.show_books()
            case 6:
                lib.view_members()
            case 7:
                break
            case _:
                lib_utils.print_and_log_warn_message("Invalid choice, try again.")
                time.sleep(2)
                continue
    print("\nThank you for choosing us!")
    time.sleep(2)
    logger.info("Application ended.")
    os.system("cls")

if __name__ == '__main__':
    main()