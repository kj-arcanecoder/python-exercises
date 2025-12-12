class Account:
    """ Parent class for all bank accounts, used to maintain basic account information.
    """
    def __init__(self, account_number, account_holder, balance, pin, account_type):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.pin = pin
        self.account_type = account_type

    def deposit(deposit_amount):
        pass

    def withdraw(withdraw_amount):
        pass
    
    def display_balance():
        pass
    
    def to_dict(self):
        return {self.account_number:{
            "account_holder" : self.account_holder,
            "balance" : self.balance,
            "pin" : self.pin,
            "type" : self.account_type
        }}