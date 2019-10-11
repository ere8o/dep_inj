import config

class Operation:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.is_account = False
        self.is_transaction = False
        if config.ACCOUNT_IDENTIFIER in kwargs:
            self.is_account = True
        if config.TRANSACTION_IDENTIFIER in kwargs:
            self.is_transaction = True