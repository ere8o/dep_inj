import config
from models.account import Account

class AccountAuthorizer:

    def __init__(self, account, args):
        
        account_validations = [method_name for method_name in dir(self)
                                if callable(getattr(self, method_name)) and "__" not in method_name]

        for validation in account_validations:
            getattr(self, validation)(account, args)
        
        print(account.__dict__)

    def account_duplicated(self, account, args):
        if hasattr(account, config.ACCOUNT_IDENTIFIER):
            account.violations = [config.DUPLICATED_VIOLATION]
        else:
            account.__dict__.update(Account(**args).__dict__)
            account.violations = [config.NO_VIOLATIONS]

    def account_inactive(self, account, args):
        if not account.account["activeCard"]:
            account.violations = [config.NOT_ACTIVE_VIOLATION]
