from datetime import datetime

import config
from models.operation import Operation
from models.account import Account
from models.transaction import Transaction

from controllers.account_authorizer import AccountAuthorizer
from controllers.transaction_authorizer import TransactionAuthorizer


class Authorizer:

    def __init__(self, account, transactions, args):
        self.operation = Operation(**args)

        if self.operation.is_account:
            AccountAuthorizer(account, args)

        if self.operation.is_transaction:
            TransactionAuthorizer(account, transactions, args)
