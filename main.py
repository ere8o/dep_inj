import sys

from controllers.load_operations import LoadOperations
from controllers.authorizer import Authorizer

from models.account import Account

if __name__ == "__main__":

    account = Account()
    transactions = {}

    file_path = sys.argv[1]
    # file_path = "files/input"

    # Something to commit 

    for message in LoadOperations(file_path).multiple_operations():

        authorizer = Authorizer(account, transactions, message)
