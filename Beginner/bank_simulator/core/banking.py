from collections import defaultdict
from datetime import datetime
import logging
import time
from . import account
from . import saving_account
from . import checking_account
from . import utils
import os
import secrets

logger = logging.getLogger(__name__)
class Banking:
    """Maintaining all the banking operations like account creation, deposit & withdraw money, transfer money and adding interest to savings account.
    """
    def __init__(self):
        """Initializing the class by fetching all accounts data from the json file and storing it in the object.
        """
        self.get_all_accounts_from_file()

    def get_all_accounts_from_file(self):
        """fetching all accounts data from the json file and storing it in self.accounts.
        """
        self.accounts = defaultdict(list)
        count = 0
        accounts_dict = utils.get_all_accounts()
        if accounts_dict:
            for number, details in accounts_dict.items():
                if details['type'] == "savings":
                    self.accounts[number] = saving_account.SavingsAccount(number, details['account_holder'], details['balance'], details['pin'], details['type'])
                    count += 1
                elif details['type'] == "checking":
                    self.accounts[number] = checking_account.CheckingAccount(number, details['account_holder'], details['balance'], details['pin'], details['type'])
                    count += 1
            logger.info(f"Fetched {count} accounts from file.")

    def create_account(self):
        """Create a new bank account after taking input from the user.

        Raises:
            ValueError: If account type value added by the user is not savings or checking
            ValueError: If the value of the pin added by the user is not a 4 digit pin
        """
        logger.info("In create account section")
        os.system("cls")
        print("******************Create Account******************")
        try:
            account_holder = input("\nInput account holder name: ")
            account_type = input("Enter account type (savings/checking): ").lower()
            if account_type not in ["savings","checking"]:
                raise ValueError("Account type is invalid")
            account_balance = input("Enter the account balance: ")
            account_balance = self.validate_new_acc_balance(account_balance)
            pin = int(input("Enter 4 digit pin: "))
            if not (pin > 999 and pin < 10000):
                raise ValueError("Pin is invalid")
            self.processing_new_account(account_holder, account_type, account_balance, pin)
        except ValueError as e:
            print(e)
        except TypeError:
            print("Invalid value.")
        finally:
            print("\nReturning to main menu.")

    def validate_new_acc_balance(self, account_balance):
        """Validates the balance added by the user for new account creation

        Args:
            account_balance (string): Initially a string, contains balance amount of the new user account.

        Raises:
            ValueError: If the balance cannot be converted to float
            ValueError: If the balance is zero or negative

        Returns:
            account_balance: If the validation is successful.
        """
        try:
            account_balance = round(float(account_balance), 2)
        except ValueError:
            raise ValueError("Account balance is not numeric.")
        if account_balance <= 0:
            raise ValueError("Account balance cannot be zero or negative.")
        return account_balance

    def processing_new_account(self, account_holder, account_type, account_balance, pin):
        """Processing the new account data given by the user to create a new savings or checking account

        Args:
            account_holder (_type_): _description_
            account_type (_type_): _description_
            account_balance (_type_): _description_
            pin (_type_): _description_
        """
        utils.print_and_log_info_message("Processing new account details.")
        account_number = self.generate_account_number()
        if account_type == "savings":
            utils.print_and_log_info_message("Creating new savings account.")
            new_account = saving_account.SavingsAccount(account_number, account_holder, account_balance, pin, account_type)
            self.save_account(new_account)
        else:
            utils.print_and_log_info_message("Creating new checking account.")
            new_account = checking_account.CheckingAccount(account_number, account_holder, account_balance, pin, account_type)
            self.save_account(new_account)
        time.sleep(1)
            
    def save_account(self, new_account):
        """Saving the new saving or checking account to file.

        Args:
            new_account (SavingsAccount or CheckingAccount): object of child account classes - either savings or checking
        """
        new_account_dict = new_account.to_dict()
        self.accounts[new_account.account_number] = new_account
        utils.save_account(new_account_dict)

    def generate_account_number(self):
        """Generate a unique 7-digit account number that does not conflict with existing accounts."""
        digits = 7
        existing = set(str(a) for a in self.accounts.keys())
        lower, upper = 10**(digits - 1), 10**digits - 1
        while True:
            acc_num = str(secrets.randbelow(upper - lower + 1) + lower)
            if acc_num not in existing:
                utils.print_and_log_info_message(f"Generated account number {acc_num}")
                return acc_num

    def deposit_amount(self):
        """Depost a valid amount to an existing account.

        Raises:
            ValueError: When the value for the account number or deposit amount is not valid.
        """
        logger.info("In deposit account section")
        os.system("cls")
        print("******************Deposit Amount******************")
        try:
            account_number_check = input("\nEnter the account number: ")
            if account_number_check in self.accounts.keys():
                user_deposit_account = self.accounts[account_number_check]
                print(f"\nHi {self.accounts[account_number_check].account_holder}!")
                user_deposit_amount = input("\nEnter the amount to deposit: ")
                self.validate_account_pin(user_deposit_account)
                user_deposit_amount = self.validate_deposit_amount(user_deposit_amount)
                user_deposit_account.balance += user_deposit_amount
                utils.print_and_log_info_message(f"Updating the deposited amount to account {account_number_check}")
                self.save_account(user_deposit_account)
                self.update_transaction(user_deposit_account, "deposit", user_deposit_amount)
                time.sleep(1)
                print("Amount updated successfully!")
            else:
                raise ValueError("Could not find account number.")
        except ValueError as e:
            print(e)
        finally:
            print("\nReturning to main menu.")

    def validate_account_pin(self, user_account):
        """Validate the account pin before completing the transaction

        Args:
            user_account (Account): Account object of the user

        Raises:
            ValueError: When the pin validation fails after multiple attempts.
        """
        attempts_left = 3
        while attempts_left > 0:
            validate_pin = input("\nEnter the pin to validate the transaction: ")
            try:
                validate_pin = int(validate_pin)
            except ValueError:
                print("\nInvalid input. Please enter numeric digits only.")
            if validate_pin == user_account.pin:
                print("\nPIN validated successfully.")
                break
            else:
                attempts_left -= 1
                print(f"\nInvalid PIN")
            if attempts_left > 0:
                print(f"\n{attempts_left} attempts left.")
            else:
                raise ValueError("Failed to validate the account PIN.")


    def validate_deposit_amount(self, user_deposit_amount):
        """Validates the deposit amount entered by the user.

        Args:
            user_deposit_amount (float): Deposit amount entered by the user

        Raises:
            ValueError: When the amount entered is not float.
            ValueError: When the deposit amount is zero or negative.

        Returns:
            _type_: _description_
        """
        try:
            amount = round(float(user_deposit_amount), 2)
        except ValueError:
            raise ValueError("The amount entered is invalid.")
        if amount <= 0:
            raise ValueError("Deposit amount cannot be zero or negative.")
        return amount

        
    def withdraw_amount(self):
        logger.info("In withdraw account section")
        os.system("cls")
        print("******************Withdraw Amount******************")
        try:
            account_number_check = input("\nEnter the account number: ")
            if account_number_check in self.accounts.keys():
                user_withdraw_account = self.accounts[account_number_check]
                print(f"\nHi {self.accounts[account_number_check].account_holder}!")
                user_withdraw_amount = input("\nEnter the amount to withdraw: ")
                self.validate_account_pin(user_withdraw_account)
                user_withdraw_amount = self.validate_withdraw_amount(user_withdraw_amount, user_withdraw_account)
                user_withdraw_account.balance -= user_withdraw_amount
                utils.print_and_log_info_message(f"Updating the withdrawing amount to account {account_number_check}")
                self.save_account(user_withdraw_account)
                self.update_transaction(user_withdraw_account, "withdraw", user_withdraw_amount)
                time.sleep(1)
                print("Amount withdrawn successfully!")
            else:
                raise ValueError("Could not find account number.")
        except ValueError as e:
            print(e)
        finally:
            print("\nReturning to main menu.")
            
    def validate_withdraw_amount(self, user_withdraw_amount, user_withdraw_account):
        """Validates the withdraw amount entered by the user.

        Args:
            user_withdraw_amount (float): Deposit amount entered by the user
            user_withdraw_account (Account): Account of the user

        Raises:
            ValueError: When the amount entered is not float.
            ValueError: When the deposit amount is zero or negative.

        Returns:
            float: the amount to withdraw post validation
        """
        try:
            amount = round(float(user_withdraw_amount), 2)
        except ValueError:
            raise ValueError("The amount entered is invalid.")
        if amount <= 0:
            raise ValueError("Amount cannot be zero or negative.")
        if (amount > user_withdraw_account.balance 
            and user_withdraw_account.account_type =='savings'
        ) or (
            user_withdraw_account.account_type =='checking' 
            and (amount > (user_withdraw_account.balance + user_withdraw_account.overdraft_limit))
        ):
            raise ValueError("Amount is greater than balance.")
        return amount
    
    def update_transaction(self, account, transaction_type, amount):
        """Adding transactions details to dictionary before saving it to file 

        Args:
            account (Account): The account object of the customer
            transaction_type (str): Type of transaction
            amount (float): Total amount
        """
        current_date_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        transaction_key = account.account_number + "-" + current_date_time
        transaction_to_save = {transaction_key:{
            "transaction_type" : transaction_type,
            "amount" : amount,
            "time" : current_date_time
        }}
        utils.save_transactions(transaction_to_save)

    def transfer_amount(self):
        """Transfers the amount from one account to another

        Raises:
            ValueError: When source account number is not found
            ValueError: Warget target account number is not found
        """
        logger.info("In transfer amount section")
        os.system("cls")
        print("******************Transfer Amount******************")
        try:
            source_account_number = input("\nEnter the account number: ")
            if not source_account_number in self.accounts.keys():
                raise ValueError("Could not find account number.")
            target_account_number = input("\nEnter the account number to transfer the amount to: ")
            if not target_account_number in self.accounts.keys():
                raise ValueError("Could not find account number.")
            source_account = self.accounts[source_account_number]
            target_account = self.accounts[target_account_number]
            amount = input(f"Enter the amount to be transferred from {source_account_number}: ")
            amount = self.validate_withdraw_amount(amount, source_account)
            source_account.balance -= amount
            target_account.balance += amount
            self.save_account(source_account)
            self.save_account(target_account)
            self.update_transaction(source_account, "trasfer_source", amount)
            self.update_transaction(target_account, "trasfer_target", amount)
            time.sleep(2)
            utils.print_and_log_info_message(f"Transfer successful from {source_account_number} to {target_account_number}")
        except ValueError as e:
            print(e)
        finally:
            print("\nReturning to main menu.")

    def add_interest(self):
        """Adds interest to the savings account

        Raises:
            ValueError: If the account number added by user is a checking account
            ValueError: If account number does not exist
        """
        logger.info("In add interest section")
        os.system("cls")
        print("******************Add Interest******************")
        try:
            account_number_check = input("\nEnter the account number: ")
            if account_number_check in self.accounts.keys():
                print(f"\nHi {self.accounts[account_number_check].account_holder}!")
                user_savings_account = self.accounts[account_number_check]
                if user_savings_account.account_type == 'checking':
                    raise ValueError("Cannot add interest to checking account.")
                print(f"Adding interest to account {account_number_check}")
                interest = user_savings_account.interest_rate / 100
                user_savings_account.balance += user_savings_account.balance * interest
                self.save_account(user_savings_account)
                self.update_transaction(user_savings_account, "interest", interest)
                time.sleep(2)
                utils.print_and_log_info_message(f"Interest added to account {account_number_check}")
            else:
                raise ValueError("Could not find account number.")
        except ValueError as e:
            print(e)
        finally:
            print("\nReturning to main menu.")

    def show_all_accounts(self):
        """Fetches all bank accounts and displays the information for each account.
        """
        logger.info("Fetching all accounts to display.")
        os.system("cls")
        print("******************Deposit Amount******************")
        print(f"{'Account Number':<15} {'Name':<20} {'Balance':<15} {'Account Type':<15}")
        for account_number, details  in self.accounts.items():
            print(f"{account_number:<15} {details.account_holder:<20} {details.balance:<15} {details.account_type:<10}")
        input("\nPress Enter to continue...")