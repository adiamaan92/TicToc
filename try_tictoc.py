import copy
import re

import scenarios_tictoc as scenarios
from Queries import populate_user
from Tictoc import Tictoc
from Transaction import Transaction_TicToc

no_transactions = 0
user_list = populate_user(100, db=True)
Tran_dict = dict()
arg_list = dict()
command_list = list()
temp_list = copy.deepcopy(user_list)
algorithm = Tictoc(temp_list)
text = scenarios.scene.splitlines()

def algo_parser(text):
    global no_transactions
    for i in text:
        if re.match(r'T\s=\s\d+', i):
            trx_match = re.match(r'T\s=\s(\d+)', i)
            no_transactions = int(trx_match.group(1))
        elif re.match(r'.\s=\s\d+', i):
            arg_match = re.match(r'(.)\s=\s(\d+)', i)
            arg_list[arg_match.group(1)] = int(arg_match.group(2))
        elif re.match(r'READ(\d+)\(.*\)', i):
            read_match = re.match(r'READ(\d+)\((.*)\)?', i)
            command_list.append(['R', read_match.group(1), read_match.group(2)])
        elif re.match(r'WRITE(\d+)\(.*\)', i):
            write_match = re.match(r'WRITE(\d+)\((.*)\)?', i)
            command_list.append(['W', write_match.group(1), write_match.group(2)])
        elif re.match(r'COMMIT(\d+)', i):
            commit_match = re.match(r'COMMIT(\d+)', i)
            command_list.append(['C', commit_match.group(1), None])


algo_parser(text)
for i in range(1, no_transactions + 1):
    key = "T" + str(i)
    Tran_dict[key] = Transaction_TicToc(copy.deepcopy(user_list))

# TODO : get more examples for serialization and non serialization transaction to make a robust test

algorithm.control_logic(Tran_dict, arg_list, command_list)
