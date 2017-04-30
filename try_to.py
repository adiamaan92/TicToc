import copy
import re

from TO import TimeStamp
from Transaction import Transaction_TS
from Queries import populate_user
import scenarios

user_list = populate_user(100, db=False)
Tran_dict = dict()
arg_list = dict()
command_list = list()
temp_list = copy.deepcopy(user_list)
algorithm = TimeStamp(temp_list)
no_transactions = 0
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
        elif re.match(r'READ(\d+)\(.\)', i):
            read_match = re.match(r'READ(\d+)\((.)\)?', i)
            command_list.append(['R', read_match.group(1), read_match.group(2)])
        elif re.match(r'WRITE(\d+)\(.\)', i):
            write_match = re.match(r'WRITE(\d+)\((.)\)?', i)
            command_list.append(['W', write_match.group(1), write_match.group(2)])
        elif re.match(r'COMMIT(\d+)', i):
            commit_match = re.match(r'COMMIT(\d+)', i)
            command_list.append(['C', commit_match.group(1), None])


algo_parser(text)
set_time = 0
for i in range(no_transactions + 1, 1, -1):
    set_time += 1
    key = "T" + str(i)
    Tran_dict[key] = Transaction_TS(set_time, algorithm)


algorithm.control_logic(Tran_dict, arg_list, command_list)

