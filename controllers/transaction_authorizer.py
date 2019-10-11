from datetime import datetime

import config
from models.transaction import Transaction


class TransactionAuthorizer:

    def __init__(self, account, transactions, args):

        transaction = Transaction(**args)

        transaction_validations = [method_name for method_name in dir(self)
                                   if callable(getattr(self, method_name)) and
                                   "__" not in method_name and
                                   config.TRANSACTION_IDENTIFIER in method_name]

        valid_transaction = False
        for validation in transaction_validations:
            valid_transaction = getattr(self, validation)(
                account, transaction, transactions, args)
            if not valid_transaction:
                break

        if valid_transaction:
            self.store(account, transaction, transactions)
        print(account.__dict__)

    def store(self, account, transaction, transactions):
        availableLimit = account.account["availableLimit"] - \
            transaction.transaction.amount
        account.account["availableLimit"] = availableLimit
        account.violations = [config.NO_VIOLATIONS]
        transactions[len(transactions)] = transaction

    def transaction_insufficient_founds(self, account, transaction, transactions, args):

        ct_amount = transaction.transaction.amount

        availableLimit = account.account["availableLimit"] - ct_amount
        if availableLimit < config.MIN_CREDIT_LIMIT:
            account.violations = [config.NO_FOUNDS_VIOLATION]
            return False
        return True

    def transaction_card_not_active(self, account, transaction, transactions, args):
        if not account.account["activeCard"]:
            account.violations = [config.NOT_ACTIVE_VIOLATION]
            return False
        return True

    def transaction_minimum_interval(self, account, transaction, transactions, args):
        if transactions:

            if len(transactions) + 1 > config.MIN_PREVIOUS_TRANSACTIONS:

                last_transaction = transactions[len(transactions) - config.MIN_PREVIOUS_TRANSACTIONS]

                lt_time = datetime.strptime(
                    last_transaction.transaction.time, config.DATETIME_FORMAT)

                ct_time = datetime.strptime(
                    transaction.transaction.time, config.DATETIME_FORMAT)

                time_diff = ct_time - lt_time
                time_diff_sec = time_diff.seconds
                if time_diff_sec < config.MIN_SECONDS_INTERVAL:
                    account.violations = [config.INTERVAL_VIOLATION]
                    return False
        return True

    def transaction_doubled_transaction(self, account, transaction, transactions, args):
        
        if transactions:

            ct_merchant = transaction.transaction.merchant
            ct_ammount =  transaction.transaction.amount
            ct_time = datetime.strptime(
                transaction.transaction.time, config.DATETIME_FORMAT)

            for item in transactions.values():

                merchant = item.transaction.merchant
                ammount = item.transaction.amount
                time = datetime.strptime(
                    item.transaction.time, config.DATETIME_FORMAT)

                if ct_merchant == merchant and ct_ammount == ammount:
                    
                    time_diff = ct_time - time
                    time_diff_sec = time_diff.seconds
                    if time_diff_sec < config.MIN_SECONDS_INTERVAL:
                        account.violations = [config.DOUBLED_TRANSACTION_VIOLATION]
                        return False
        return True
