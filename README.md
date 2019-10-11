# Account / Transactions Authorizer

### Introduction:
This is a python based command line program to a create single ***account*** and
validate its ***transactions***. The program reads JSON lines from an input plain
text file and processes them each at the time through different validation rules, 
and finally prints to standard output the validation result of processes.

### Requirements:
1. Python 3
2. pytest

### Running:
1. Run [**python main.py PATH\TO\INPUTFILE**]
2. Run tests with [**pytest test_authorizer.py**]

### Design:
* The program stands on a structure similar to mvc, for the sake of the program simplicity 
the controller outputs the final state of the operation.
* There has also been implemented a helper method to read/load the input file one JSON line
at the time. 
* Validation rules are separated according to their nature in Account Validations and 
Transaction Validations. 
* Each message is validated against the specific rules for its type.
* Each validation it's self contained in it's own method and new rules can be added in the 
same manner. 
* New rules are automatically identified as long as they are named with the prefix "account_" 
or "transaction_".
