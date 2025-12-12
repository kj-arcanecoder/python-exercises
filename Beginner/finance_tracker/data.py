import state
import time
import os

def read_transactions_from_file():
    if not os.path.exists('transactions.txt'):
        return []
    all_transactions =[]
    with open('transactions.txt', encoding="utf-8") as f:
        for line in f:
            type, description, amount, date = line.strip().split(",")
            all_transactions += ((type, description, float(amount), date),)
    return all_transactions

def export_to_file():
    transactions_to_export = state.print_unsaved_transactions()
    if transactions_to_export:
        print("\n\nAbove transactions will now be saved to file.",end="")
        for _ in range(4):
            print(".", end="", flush=True)
            time.sleep(1)
        unsaved_transactions = state.get_unsaved_transactions()
        with open('transactions.txt', 'a',encoding="utf-8") as f:
            for type, description, amount, date in unsaved_transactions:
                f.write(f"{type},{description},{amount},{date}\n")
        print("\n\nAll transactions saved successfully.")
        state.clear_transactions()
        time.sleep(3)
    else:
        print("\nNo transactions to save.")
        time.sleep(3)