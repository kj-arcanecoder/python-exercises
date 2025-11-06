from . import account

class CheckingAccount(account.Account):
    """ Child class of Account, used to maintain savings account specific information.

    Args:
        account (_type_): Account parent class
    """
    def __init__(self, account_number, account_holder, balance, pin, account_type):
        super().__init__(account_number, account_holder, balance, pin, account_type)
        self.overdraft_limit = 20000.00

    def withdraw(withdraw_amount):
        pass
        # return super().withdraw()
