import state
import data as data
import time
from datetime import datetime, date

def add_transaction(type_):
    description = input(f"Enter description for {type_}: ").lower()
    amount = float(input("Enter amount: "))
    t_date = input("Enter date DD-MM-YYYY (leave blank for today): ")
    if not t_date:
        t_date = date.today().strftime("%d-%m-%Y")
    else:
        t_date = datetime.strptime(t_date, "%d-%m-%Y").strftime("%d-%m-%Y")
    state.add_transaction(type_, description, amount, t_date)
    print("\nTransaction added (unsaved). Returning to menu...")
    time.sleep(2)

def view_summary():
    saved_transactions = data.read_transactions_from_file()
    total_income = float(0)
    total_expense = float(0)
    net_savings = float(0)
    expense_breakdown = {}

    if saved_transactions:
        for type, description, amount, date in saved_transactions:
            if type == 'Income':
                total_income += amount
            else:
                total_expense += amount
            if description in expense_breakdown:
                expense_breakdown[description] += amount
            else:
                expense_breakdown[description] = amount
        net_savings = total_income - total_expense
        print(f"\nTotal Income: {total_income}")
        print(f"Total Expense: {total_expense}")
        print(f"Net Savings: {net_savings}")

        print("\n\nExpense Breakdown:")
        for type, amount in expense_breakdown.items():
            print(f"{type}: {amount}")
        input("\n\nPress Enter to continue...")
    else:
        print("\nNo transactions to display.")
        input("\n\nPress Enter to continue...")

def view_transactions_history():
    saved_transactions = data.read_transactions_from_file()
    if saved_transactions:
        print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':>10}")
        for t_type, desc, amt, t_date in saved_transactions:
            print(f"{t_date:<12} {t_type:<10} {desc:<15} {amt:>10.2f}")

        input("\n\nPress Enter to continue...")
    else:
        print("\nNo transactions to display.")
        input("\n\nPress Enter to continue...")
        

def export_to_file():
    data.export_to_file()
