import file_utils
import time

def add_item(inventory):
    name = input("Enter name of the product: ")
    price = 0.0
    quantity = 0
    try:
        price = float(input("Enter price: "))
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid value, returning to main menu.")
        time.sleep(2)
        return

    inventory[name] = dict({"price":price, "quantity":quantity})
    file_utils.save_inventory(inventory)

def update_price(inventory):
    name = input("Enter name of the product: ")
    if name in inventory:
        try:
            price = float(input("Enter new price: "))
            inventory[name]["price"] = price
        except ValueError:
            print("Invalid value, returning to main menu.")   
            time.sleep(2)
            return 
    else:
        print("Product not found.")
        time.sleep(2)
        return
    file_utils.save_inventory(inventory)
    print("Price updated successfully.")
    time.sleep(2)


def remove_item(inventory):
    name = input("Enter name of the product: ")
    if name in inventory:
        del inventory[name]
        file_utils.save_inventory(inventory)
        print("Product deleted successfully")
    else:
        print("No product found to delete")
    time.sleep(2)

def purchase_item(inventory):
    name = input("Enter name of the product you want to purchase: ")
    if name in inventory:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= inventory[name]["quantity"]:
                inventory[name]["quantity"] -= quantity
                file_utils.save_inventory(inventory)
                print(f"Item purchased, {inventory[name]["quantity"]} quantity left")
                cost = inventory[name]["price"] * quantity
                print(f"Total cost= {cost}")
                file_utils.save_transaction(name, quantity, cost)               
            elif quantity <= 0:
                raise ValueError("Quantity cannot be less than or equal to 0")
            elif quantity > inventory[name]["quantity"]:
                raise ValueError("Insufficient quantity, returning to menu.")
        except ValueError as e:
            print(e)
            time.sleep(2)
    else:
        print("Product does not exist, returning to menu.")
        time.sleep(2)
    time.sleep(2)

def view_inventory(inventory):
    print(f"\n{'='*45}")
    print(f"{'Name':<20} {'Price(₹)':<10} {'Quantity':<10}")
    print(f"{'-'*45}")
    for name, details in inventory.items():
        print(f"{name:<20} {details['price']:<10.2f} {details['quantity']:<10}")
    print(f"{'='*45}")

    input("\nPress enter to continue.")
