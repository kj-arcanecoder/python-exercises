import sys


class OnlineStore:
    def __init__(self):
        self.total = 0
        self.cart = {}

    def show_menu(self):
        print("************** Online Store *************")
        print("1. View store items")
        print("2. Add item to cart")
        print("3. Remove item from cart")
        print("4. View cart")
        print("5. Checkout and exit")

    def take_input(self):
        choice = int(input("Enter your choice: "))
        match choice:
            case choice if choice == 1:
                self.view_items()
            case choice if choice == 2:
                self.add_to_cart()
            case choice if choice == 3:
                self.remove_from_cart()
            case choice if choice == 4:
                self.view_cart()
            case choice if choice == 5:
                self.checkout()
            case _:
                print("Invalid choice")
    
    def view_items(self):
        print("************** Products List *************")
        print("1. Apple = Rs. 100")
        print("2. Banana = Rs. 30")
        print("3. Milk = Rs. 70")
        print("4. Bread = Rs. 50")
        print("5. Eggs = Rs. 80")
        print("-------------------------------------------")

    def add_to_cart(self):
        item_to_add = int(input("Enter the item number to be added to cart: "))
        match item_to_add:
            case item_to_add if item_to_add == 1:
                if "apple" in self.cart:
                    self.cart["apple"]["total"] += 100
                    self.cart["apple"]["quantity"] += 1
                else:
                    self.cart["apple"] = {"total": 100, "quantity": 1}
                print("Apple added to cart successfully.")
            case item_to_add if item_to_add == 2:
                if "banana" in self.cart:
                    self.cart["banana"]["total"] += 30
                    self.cart["banana"]["quantity"] += 1
                else:
                    self.cart["banana"] = {"total": 30, "quantity": 1}
                print("Banana added to cart successfully.")
            case item_to_add if item_to_add == 3:
                if "milk" in self.cart:
                    self.cart["milk"]["total"] += 70
                    self.cart["milk"]["quantity"] += 1
                else:
                    self.cart["milk"] = {"total": 70, "quantity": 1}
                print("Milk added to cart successfully.")
            case item_to_add if item_to_add == 4:
                if "bread" in self.cart:
                    self.cart["bread"]["total"] += 50
                    self.cart["bread"]["quantity"] += 1
                else:
                    self.cart["bread"] = {"total": 50, "quantity": 1}
                print("Bread added to cart successfully.")
            case item_to_add if item_to_add == 5:
                if "eggs" in self.cart:
                    self.cart["eggs"]["total"] += 80
                    self.cart["eggs"]["quantity"] += 1
                else:
                    self.cart["eggs"] = {"total": 80, "quantity": 1}
                print("Eggs added to cart successfully.")
    
    def remove_from_cart(self):
        item_to_remove = int(input("Enter the item number to be removed: "))
        match item_to_remove:
            case item_to_remove if item_to_remove == 1:
                if self.cart["apple"]["quantity"] > 1:
                    self.cart["apple"]["quantity"] -= 1
                    self.cart["apple"]["total"] -= 100
                else:
                    del self.cart["apple"]
                print("Apple removed!")
            case item_to_remove if item_to_remove == 2:
                if self.cart["banana"]["quantity"] > 1:
                    self.cart["banana"]["quantity"] -= 1
                    self.cart["banana"]["total"] -= 30
                else:
                    del self.cart["banana"]
                print("Banana removed!")
            case item_to_remove if item_to_remove == 3:
                if self.cart["milk"]["quantity"] > 1:
                    self.cart["milk"]["quantity"] -= 1
                    self.cart["milk"]["total"] -= 70
                else:
                    del self.cart["milk"]
                print("Milk removed!")
            case item_to_remove if item_to_remove == 4:
                if self.cart["bread"]["quantity"] > 1:
                    self.cart["bread"]["quantity"] -= 1
                    self.cart["bread"]["total"] -= 60
                else:
                    del self.cart["bread"]
                print("Bread removed!")
            case item_to_remove if item_to_remove == 5:
                if self.cart["eggs"]["quantity"] > 1:
                    self.cart["eggs"]["quantity"] -= 1
                    self.cart["eggs"]["total"] -= 80
                else:
                    del self.cart["eggs"]
                print("Eggs removed!")
            case _:
                print("Invalid choice!")

    def view_cart(self):
        print("Product     Quantity      Total")
        for item, info in self.cart.items():
            print(f"{item}     {info['quantity']}     {info['total']}")

    def checkout(self):
        print("Order placed successfully! Here's your order summary")
        self.view_cart()
        for item in self.cart:
            self.total += self.cart[item]["total"]
        print(f"Order total = {self.total}")
        sys.exit()

def main():
    onlineStore = OnlineStore()
    continue_shop = True
    while continue_shop:
        onlineStore.show_menu()
        onlineStore.take_input()

main()