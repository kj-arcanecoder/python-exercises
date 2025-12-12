import logging
import time
from core import contact_book
from core import utils as address_utils
import logging_config

logging_config.setup_logging()
logger = logging.getLogger(__name__)

def show_menu():
    """Display the main menu
    """
    address_utils.print_header("Address Manager")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Edit Contact")
    print("5. Delete Contact")
    print("6. Export All Contacts to CSV File")
    print("7. Exit")

def main():
    """The starting point of the address manager
    """
    logger.info("Address manager application started.")
    choice = 0
    address_book = contact_book.ContactBook()
    menu_loop(choice, address_book)
    logger.info("Address manager application ended.") 

def menu_loop(choice, address_book):
    """Maintains the menu loop until the user chooses to exit the app.

    Args:
        choice (int): the choice entered by the user
        address_book (ContactBook): Object of ContactBook class, to call any of the CRUD operations requested by the user
    """
    while choice != 7:
        address_utils.clear_cli()
        show_menu()
        try:
            choice = int(input("\nEnter input: "))
        except ValueError:
            print("\n Invalid input, try again.")
            time.sleep(2)
            continue
        match choice:
            case 1:
                address_book.add_contact()
            case 2:
                address_book.view_all_contacts()
            case 3:
                address_book.search_contacts()
            case 4:
                address_book.edit_contact()
            case 5:
                address_book.delete_contact()
            case 6:
                address_book.export_to_csv()
            case 7:
                print("Thank you for using this app.")
            case _:
                print("\n Invalid input, try again.")
        
if __name__=='__main__':
    main()