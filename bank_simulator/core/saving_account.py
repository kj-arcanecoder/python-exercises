from . import account

class SavingsAccount(account.Account):
    """ Child class of Account, used to maintain savings account specific information.

    Args:
        account (_type_): Account parent class
    """
    def __init__(self, account_number, account_holder, balance, pin, account_type):
        super().__init__(account_number, account_holder, balance, pin, account_type)
        self.interest_rate = 7

    def add_interest():
        pass