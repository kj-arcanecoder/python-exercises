import logging
import os
import time
from core import banking as banking_ops
from logging_config import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

def show_menu():
    os.system("cls")
    print("******************Bank Simulator******************")
    print("\n1. Create account (savings/checking)")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. Transfer money between accounts")
    print("5. Add interest (for savings)")
    print("6. Display all accounts")
    print("7. Exit")

def main():
    """The starting point of the banking application

    Raises:
        ValueError: When the choice entered is not from the provided choices.
    """
    choice = 0
    banking = banking_ops.Banking()
    while choice != 7:
        show_menu()
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("\nInvalid choice, try again.")
            time.sleep(2)
            continue
        match choice:
            case 1:
                banking.create_account()
            case 2:
                banking.deposit_amount()
            case 3:
                banking.withdraw_amount()
            case 4:
                banking.transfer_amount()
            case 5:
                banking.add_interest()
            case 6:
                banking.show_all_accounts()
            case 7:
                print("\nThank you for banking with us!")
            case _:
                try:
                    raise ValueError
                except ValueError:
                    print("\nInvalid choice, try again.")
        time.sleep(2)            
        
if __name__ == '__main__':
    main()