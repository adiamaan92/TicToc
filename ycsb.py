import copy
import re
import random
import math
from random import Random
from Queries import populate_user
from Tictoc import Tictoc
from Transaction import Transaction_TicToc, Transaction_TS
import time
from TO import TimeStamp
import string


no_transactions = 0
data_size = 10000
contention_size = int(data_size * 0.1)
user_list = populate_user(data_size, db=False)
Tran_dict = dict()
arg_list = dict()
command_list = list()
temp_list = copy.deepcopy(user_list)
algorithm1 = Tictoc(temp_list)
algorithm2 = TimeStamp(temp_list)

# for randomly generating the data
myPRNG = Random()

no_of_queries = 8
no_of_reads = 6
no_of_writes = no_of_queries - no_of_reads
hotspot_queries = 0.6
no_of_comm_users = int(math.ceil(no_of_queries * hotspot_queries))

# number of transactions occurring concurrently
trans_reqd = 20

# number of commit statements in medium contention and
# high contention of the queries
count = 0

# Number of times the transaction will get aborted
abort = 0


# To generate the rows which will be common for
# x% of the queries.
comm_user_id = []
for i in range(contention_size):
    comm_user_id.append(myPRNG.randint(0, data_size))


# To generate the transaction commands for a
# transaction.
def create_trans(trans_no, flag):
    alpha = list(string.ascii_uppercase)
    key = alpha[:no_of_comm_users]
    not_comm = alpha[no_of_comm_users:20]
    not_comm.remove('T')
    random.shuffle(key)
    # random.shuffle(not_comm)
    # print key
    if flag == "read_queries":
        trans_command = [''] * no_of_queries
        j = 0
        while j < no_of_queries:
            rand = myPRNG.randint(0, no_of_queries - 1)
            if trans_command[rand] == 'READ':
                continue
            else:
                j += 1
                trans_command[rand] = 'READ'
        for i in range(no_of_comm_users):
            trans_command[i] += str(trans_no) + '(' + key[i] + ')\n'
        for i in range(no_of_queries):
            if '(' in trans_command[i]:
                continue
            else:
                trans_command[i] += str(trans_no) + '(' + not_comm[myPRNG.randint(0, 18 - no_of_comm_users)] + ')\n'
        random.shuffle(trans_command)

        return trans_command

    elif flag == "med_contention":
        no_of_reads = 6
        no_of_writes = no_of_queries - no_of_reads
        trans_command = [''] * no_of_queries
        j = 0
        while j < no_of_reads:
            rand = myPRNG.randint(0, no_of_queries - 1)
            if trans_command[rand] == 'READ':
                continue
            else:
                j += 1
                trans_command[rand] = 'READ'
        for i in range(no_of_queries):
            if trans_command[i] == '':
                trans_command[i] = 'WRITE'
        for i in range(no_of_comm_users):
            trans_command[i] += str(trans_no) + '(' + key[i] + ')\n'
        for i in range(no_of_queries):
            if '(' in trans_command[i]:
                continue
            else:
                trans_command[i] += str(trans_no) + '(' + not_comm[myPRNG.randint(0, 18 - no_of_comm_users)] + ')\n'
        random.shuffle(trans_command)

        return trans_command

    else:
        no_of_reads = 4
        no_of_writes = 4
        trans_command = [''] * no_of_queries
        j = 0
        while j < no_of_reads:
            rand = myPRNG.randint(0, no_of_queries - 1)
            if trans_command[rand] == 'READ':
                continue
            else:
                j += 1
                trans_command[rand] = 'READ'
        for i in range(no_of_queries):
            if trans_command[i] == '':
                trans_command[i] = 'WRITE'
        for i in range(no_of_comm_users):
            trans_command[i] += str(trans_no) + '(' + key[i] + ')\n'
        for i in range(no_of_queries):
            if '(' in trans_command[i]:
                continue
            else:
                trans_command[i] += str(trans_no) + '(' + not_comm[myPRNG.randint(0, 18 - no_of_comm_users)] + ')\n'
        random.shuffle(trans_command)

        return trans_command


commit_read_only = 0
commit_medium_contention = 0
commit_high_contention = 0


# evaluate 3 different variations of the workload
# Below we will evaluate 3 different variations of workload
def read_only():
    variable_value = {}
    global trans_reqd, commit_read_only
    total_trans_read = []
    total_trans_read_to = []
    flag = "read_queries"
    for i in range(1, trans_reqd + 1):
        total_trans_read += create_trans(i, flag)

    random.shuffle(total_trans_read)

    commit_read_only = len(total_trans_read)
    total_trans_read = ['T = ' + str(trans_reqd) + '\n'] + total_trans_read
    # print total_trans_read
    for i in range(len(total_trans_read)):
        if '(' in total_trans_read[i]:
            variable_name = total_trans_read[i].split('(')[1][0]
            if variable_value.has_key(variable_name):
                continue
            elif variable_name in ['A', 'B', 'C', 'D', 'E']:
                variable_value[variable_name] = comm_user_id[myPRNG.randint(0, contention_size-1)]
            else:
                variable_value[variable_name] = myPRNG.randint(0, data_size)
    # print variable_value
    for entry in variable_value:
        # print entry, variable_value[entry]
        total_trans_read.insert(1, entry + ' = ' + str(variable_value[entry]) + '\n')

    # print ''.join(total_trans_read)
    total_trans_read_to = [','.join(['T' + str(i + 1) for i in range(trans_reqd)]) + '\n']\
                          + total_trans_read

    ycsb_test = ''.join(total_trans_read)
    ycsb_test_to = ''.join(total_trans_read_to)
    # print ycsb_test_to
    return ycsb_test, ycsb_test_to


def medium_contention():
    global trans_reqd, commit_medium_contention
    variable_value = {}
    total_trans = []
    total_trans_read_to = []
    flag = "med_contention"
    for i in range(1, trans_reqd + 1):
        total_trans += create_trans(i, flag)

    random.shuffle(total_trans)

    total_trans = ['T = ' + str(trans_reqd) + '\n'] + total_trans
    for i in range(len(total_trans)):
        if '(' in total_trans[i]:
            variable_name = total_trans[i].split('(')[1][0]
            if variable_value.has_key(variable_name):
                continue
            elif variable_name in ['A', 'B', 'C', 'D', 'E']:
                variable_value[variable_name] = comm_user_id[myPRNG.randint(0, contention_size - 1)]
            else:
                variable_value[variable_name] = myPRNG.randint(0, data_size)
    # print variable_value
    for entry in variable_value:
        # print entry, variable_value[entry]
        total_trans.insert(1, entry + ' = ' + str(variable_value[entry]) + '\n')
    length = len(total_trans)
    i = 0
    commit_medium_contention = 0
    # for i in range(len(total_trans)):
    while i < length:
        if 'WRITE' in total_trans[i]:
            breakup = total_trans[i].split('(')[0][5:]
            total_trans.insert(i + 1, 'COMMIT' + breakup + '\n')
            length += 1
            commit_medium_contention += 1
        i += 1

    total_trans_read_to = [','.join(['T' + str(i + 1) for i in range(trans_reqd)]) + '\n'] \
                          + total_trans
    ycsb_test_to = ''.join(total_trans_read_to)
    ycsb_test = ''.join(total_trans)

    return ycsb_test, ycsb_test_to


def high_contention():
    global trans_reqd, commit_high_contention
    variable_value = {}
    total_trans = []
    flag = "high_contention"
    for i in range(1, trans_reqd + 1):
        total_trans += create_trans(i, flag)

    random.shuffle(total_trans)

    total_trans = ['T = ' + str(trans_reqd) + '\n'] + total_trans
    for i in range(len(total_trans)):
        if '(' in total_trans[i]:
            variable_name = total_trans[i].split('(')[1][0]
            if variable_value.has_key(variable_name):
                continue
            elif variable_name in ['A', 'B', 'C', 'D', 'E', 'F']:
                variable_value[variable_name] = comm_user_id[myPRNG.randint(0, contention_size - 1)]
            else:
                variable_value[variable_name] = myPRNG.randint(0, data_size)
    # print variable_value
    for entry in variable_value:
        # print entry, variable_value[entry]
        total_trans.insert(1, entry + ' = ' + str(variable_value[entry]) + '\n')

    length = len(total_trans)
    i = 0
    commit_high_contention = 0
    # for i in range(len(total_trans)):
    while i < length:
        if 'WRITE' in total_trans[i]:
            breakup = total_trans[i].split('(')[0][5:]
            total_trans.insert(i + 1, 'COMMIT' + breakup + '\n')
            length += 1
            commit_high_contention += 1
        i += 1
    total_trans_read_to = [','.join(['T' + str(i + 1) for i in range(trans_reqd)]) + '\n'] \
                          + total_trans
    ycsb_test_to = ''.join(total_trans_read_to)
    ycsb_test = ''.join(total_trans)
    # print ycsb_test
    return ycsb_test, ycsb_test_to


def initiate_transaction(trx_list):
    global set_time
    set_time = 0
    for i in trx_list:
        set_time += 1
        key = "T" + str(i)
        Tran_dict[key] = Transaction_TS(set_time, algorithm2)


def algo_parser(text, flag):
    global no_transactions
    if flag == "tictoc":
        no_transactions = 0
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
    else:
        no_transactions = 0
        for i in text:
            if re.match(r'^T\d+,', i):
                trx_list = re.findall(r'T(\d+)', i)
                initiate_transaction(trx_list)
            elif re.match(r'T\s=\s\d+', i):
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


# store the results of three different variations of workload
read_only_results, read_only_results_to = read_only()
medium_contention_results, medium_contention_results_to = medium_contention()
high_contention_results, high_contention_results_to = high_contention()


# testing and comparing the two algorithms
def test_tictoc1():
    global abort, commit_read_only
    text1 = read_only_results.splitlines()
    flag = "tictoc"
    abort = 0
    start_time = time.time()
    algo_parser(text1, flag)
    for i in range(1, no_transactions + 1):
        key = "T" + str(i)
        Tran_dict[key] = Transaction_TicToc(copy.deepcopy(user_list))

    algorithm1.control_logic(Tran_dict, arg_list, command_list, detailed=False)
    for k, v in Tran_dict.items():
        if v.status == "Aborted":
            abort += 1
    print ("Total number of commits: ")
    print (commit_read_only)
    print ("Total number of aborts: ")
    print (str(abort))
    print("Time taken to run tictoc with read only statements" + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n')


def test_tictoc2():
    global abort, commit_medium_contention
    text2 = medium_contention_results.splitlines()
    flag = "tictoc"
    abort = 0
    start_time = time.time()
    algo_parser(text2, flag)
    for i in range(1, no_transactions + 1):
        key = "T" + str(i)
        Tran_dict[key] = Transaction_TicToc(copy.deepcopy(user_list))

    algorithm1.control_logic(Tran_dict, arg_list, command_list, detailed=False)
    for k, v in Tran_dict.items():
        if v.status == "Aborted":
            abort += 1
    print ("Total number of commits: ")
    print (commit_medium_contention)
    print ("Total number of aborts: ")
    print (str(abort))
    print("Time taken to run tictoc with medium contention level: " + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n')


def test_tictoc3():
    global abort, commit_high_contention
    text3 = high_contention_results.splitlines()
    flag = "tictoc"
    abort = 0
    start_time = time.time()
    algo_parser(text3, flag)
    for i in range(1, no_transactions + 1):
        key = "T" + str(i)
        Tran_dict[key] = Transaction_TicToc(copy.deepcopy(user_list))

    algorithm1.control_logic(Tran_dict, arg_list, command_list, detailed=False)
    for k, v in Tran_dict.items():
        if v.status == "Aborted":
            abort += 1
    print ("Total number of commits: ")
    print (commit_high_contention)
    print ("Total number of aborts: ")
    print (abort)
    print("Time taken to run tictoc with high contention level: " + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n')


def test_to1():
    global abort, commit_read_only
    text1 = read_only_results_to.splitlines()
    flag = "timestamp"
    abort = 0
    start_time = time.time()
    algo_parser(text1, flag)

    algorithm2.control_logic(Tran_dict, arg_list, command_list, detailed=False)
    for k, v in Tran_dict.items():
        if v.status == "Aborted":
            abort += 1
    print ("Total number of commits: ")
    print (commit_read_only)
    print ("Total number of aborts: ")
    print (abort)
    print("Time taken to run timestamp with read only statements" + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n')


def test_to2():
    global abort, commit_medium_contention
    text2 = medium_contention_results_to.splitlines()
    flag = "timestamp"
    abort = 0
    start_time = time.time()
    algo_parser(text2, flag)
    algorithm2.control_logic(Tran_dict, arg_list, command_list, detailed=False)
    for k, v in Tran_dict.items():
        if v.status == "Aborted":
            abort += 1
    print ("Total number of commits: ")
    print (commit_medium_contention)
    print ("Total number of aborts: ")
    print (abort)
    print("Time taken to run timestamp with medium contention level: " + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n')


def test_to3():
    global abort, commit_high_contention
    text3 = high_contention_results_to.splitlines()
    flag = "timestamp"
    abort = 0
    start_time = time.time()
    algo_parser(text3, flag)

    algorithm2.control_logic(Tran_dict, arg_list, command_list)
    for k, v in Tran_dict.items():
        if v.status == "Aborted":
            abort += 1
    print ("Total number of commits: ")
    print (commit_high_contention)
    print ("Total number of aborts: ")
    print (abort)
    print("Time taken to run timestamp with high contention level: " + '\n')
    print("--- %s seconds ---" % (time.time() - start_time))
    print('\n')


# Test tictoc algorithms
test_tictoc1()
test_tictoc2()
test_tictoc3()
test_to1()
test_to2()
test_to3()



