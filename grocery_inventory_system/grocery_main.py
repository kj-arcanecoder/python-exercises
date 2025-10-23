import file_utils
import inventory_ops as inventory_ops
import os
import time

inventory = file_utils.load_inventory()

def print_heading():
    print("========= GROCERY INVENTORY SYSTEM =========")

def display_menu():
    os.system("cls")
    print_heading()
    print("\n1. Add Item")
    print("2. Update Price")
    print("3. Remove Item")
    print("4. View Items")
    print("5. Purchase Item")
    print("6. Exit")

def main():
    choice = 0
    while choice != 6:
        display_menu()
        try:
            choice = int(input("Enter your input: "))
        except ValueError:
            print("\nInvalid choice. Please enter a number.")
            time.sleep(2)
            continue

        match int(choice):
            case 1:
                inventory_ops.add_item(inventory)
            case 2:
                inventory_ops.update_price(inventory)
            case 3:
                inventory_ops.remove_item(inventory)
            case 4:
                inventory_ops.view_inventory(inventory)
            case 5:
                inventory_ops.purchase_item(inventory)
            case 6:
                print("Thank you!")
                time.sleep(2)
                exit()
            case _:
                print("\nInvalid choice.")
                time.sleep(2)
                continue
if __name__ == '__main__':
    main()