import json
import time

filename = "inventory.json"
transaction_filename = "transactions.json"

def load_inventory():
    print()
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found")
        time.sleep(2)
        return {}
    except json.JSONDecodeError:
        print("Corrupted file, starting fresh.")
        time.sleep(2)
        return {}

def save_inventory(inventory):
    with open(filename, "w") as f:
        json.dump(inventory, f, indent=4)

def save_transaction(product_name, quantity, cost):
    import json
import os

transaction_filename = "transactions.json"

def save_transaction(product_name, quantity, cost):
    transaction = {
        "product": product_name,
        "quantity": quantity,
        "cost": cost
    }
    if os.path.exists(transaction_filename) and os.path.getsize(transaction_filename) > 0:
        with open(transaction_filename, "r", encoding="utf-8") as f:
            try:
                transactions = json.load(f)
            except json.JSONDecodeError:
                transactions = []
    else:
        transactions = []
    transactions.append(transaction)
    with open(transaction_filename, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4)
