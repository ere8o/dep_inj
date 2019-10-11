import os
import json


class LoadOperations:

    def __init__(self, input_arg):
        self.input_arg = input_arg
        try:
            if os.stat(input_arg).st_size > 0:
                self.multiple_operations()
        except:
            print("INVALID FILE")

    def multiple_operations(self):
        with open(self.input_arg) as file_manager:
            for line in file_manager:
                yield self.process_operation(line)

    def process_operation(self, operation):
        return json.loads(operation)
