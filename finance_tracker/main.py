import finance as finance
import data as data
import os
import time

def print_heading():
    print("========= PERSONAL FINANCE PLANNER =========")

def main_menu():
    print_heading()
    print("\n1. Add Income")
    print("2. Add Expense")
    print("3. View Summary")
    print("4. View Transaction History")
    print("5. Export to File")
    print("6. Exit")

def main():
    menu_choice = 0
    while menu_choice != 6:
        os.system("cls")
        main_menu()
        menu_choice = int(input("\nInput: "))

        menu_choice = int(menu_choice)
        match menu_choice:
            case 1:
                os.system("cls")
                print_heading()
                finance.add_transaction("Income")
            case 2:
                os.system("cls")
                print_heading()
                finance.add_transaction("Expense")
            case 3:
                os.system("cls")
                print_heading()
                finance.view_summary()
            case 4:
                os.system("cls")
                print_heading()
                finance.view_transactions_history()
            case 5:
                os.system("cls")
                print_heading()
                finance.export_to_file()
            case 6:
                print("\nThank you for using Finance Planner! Stay on budget.")
                time.sleep(2)                    
            case _:
                print("Invalid choice.")
                time.sleep(2) 

if __name__=="__main__":
    main()