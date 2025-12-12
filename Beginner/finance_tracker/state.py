transactions = []

def add_transaction(type, description, amount, transaction_date):
    global transactions
    transactions.append((type, description, amount, transaction_date))

def print_unsaved_transactions():
    global transactions
    if transactions:
        print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':>10}")
        for type, description, amount, date in transactions:
            print(f"{date:<12} {type:<10} {description:<15} {amount:>10}")
        return True
    else:
        print("\nNo unsaved transactions to display.")
        return False

def get_unsaved_transactions():
    global transactions
    return transactions

def clear_transactions():
    global transactions
    transactions = []