from models.account import Account
from models.transaction import Transaction
from controllers.account_authorizer import AccountAuthorizer
from controllers.transaction_authorizer import TransactionAuthorizer

import pytest


def test_account_creation(capsys):
    args = {'account': {'activeCard': True,
                        'availableLimit': 1000}, 'violations': ['']}
    AccountAuthorizer(Account(), args)
    assert capsys.readouterr().out == \
        "{'account': {'activeCard': True, 'availableLimit': 1000}, 'violations': ['']}\n"


def test_account_duplicated(capsys):
    args = {'account': {'activeCard': True,
                        'availableLimit': 1000}, 'violations': ['']}
    AccountAuthorizer(Account(**args), args)
    assert capsys.readouterr().out == \
        "{'account': {'activeCard': True, 'availableLimit': 1000}, 'violations': ['account-already-initialized']}\n"


def test_account_inactive(capsys):
    args = {'account': {'activeCard': False,
                        'availableLimit': 1000}, 'violations': ['']}
    AccountAuthorizer(Account(**args), args)
    assert capsys.readouterr().out == \
        "{'account': {'activeCard': False, 'availableLimit': 1000}, 'violations': ['card-not-active']}\n"


def test_transaction_insufficient_founds(capsys):
    account_args = {'account': {'activeCard': True,
                                'availableLimit': 1000}, 'violations': ['']}
    transaction_args = {"transaction": {
        "merchant": "Burger King", "amount": 2000, "time": "2019-02-13T10:00:00.000Z"}}
    account = Account(**account_args)
    TransactionAuthorizer(account, {}, transaction_args)
    assert capsys.readouterr().out == \
        "{'account': {'activeCard': True, 'availableLimit': 1000}, 'violations': ['insufficient-limit']}\n"


def test_transaction_card_not_active(capsys):
    account_args = {'account': {'activeCard': False,
                                'availableLimit': 1000}, 'violations': ['']}
    transaction_args = {"transaction": {
        "merchant": "Burger King", "amount": 2000, "time": "2019-02-13T10:00:00.000Z"}}
    account = Account(**account_args)
    TransactionAuthorizer(account, {}, transaction_args)
    assert capsys.readouterr().out == \
        "{'account': {'activeCard': False, 'availableLimit': 1000}, 'violations': ['card-not-active']}\n"


def test_transaction_minimum_interval(capsys):
    account_args = {'account': {'activeCard': True,
                                'availableLimit': 1000}, 'violations': ['']}
    transaction_args = {"transaction": {
        "merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:01:30.000Z"}}
    transaction1_args = {"transaction": {
        "merchant": "Burger King", "amount": 30, "time": "2019-02-13T10:00:00.000Z"}}
    transaction2_args = {"transaction": {
        "merchant": "7 Eleven", "amount": 20, "time": "2019-02-13T10:00:30.000Z"}}
    transaction3_args = {"transaction": {
        "merchant": "Pizza Hut", "amount": 10, "time": "2019-02-13T10:01:00.000Z"}}
    account = Account(**account_args)
    transaction1 = Transaction(**transaction1_args)
    transaction2 = Transaction(**transaction2_args)
    transaction3 = Transaction(**transaction3_args)
    transactions = {0: transaction1, 1: transaction2, 2: transaction3}
    TransactionAuthorizer(account, transactions, transaction_args)
    assert capsys.readouterr().out == \
        "{'account': {'activeCard': True, 'availableLimit': 1000}, 'violations': ['high-frequency-small-intervall']}\n"


def test_transaction_doubled_transaction(capsys):
    account_args = {'account': {'activeCard': True,
                                'availableLimit': 1000}, 'violations': ['']}
    transaction_args = {"transaction": {
        "merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:30.000Z"}}
    transaction1_args = {"transaction": {
        "merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}
    account = Account(**account_args)
    transaction1 = Transaction(**transaction1_args)
    transactions = {0: transaction1}
    TransactionAuthorizer(account, transactions, transaction_args)
    assert capsys.readouterr().out == \
        "{'account': {'activeCard': True, 'availableLimit': 1000}, 'violations': ['doubled-transaction']}\n"
