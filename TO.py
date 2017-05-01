# Using a thread safe counter that increments at the start of each transaction to ensure
# unique timestamp keys
from Queries import commit_table


class TimeStamp(object):
    def __init__(self, data_list):
        self.data_list = data_list
        self.old_list = list()
        self.dependent_list = list()

    # Goes line by line of the command and handles the overall logic.
    def control_logic(self, trans_dict, arg_list, command_list, detailed=True):
        print('------------------------------------------------------------------------------') if detailed else None
        for command, transaction, records in command_list:
            t = "T" + str(transaction)
            tran = trans_dict[t]
            record = arg_list[records] if records is not None else None
            if command == 'R':
                print("--- Transaction {} ---".format(t)) if detailed else None
                if not tran.read_element(record):
                    print("!!! Transaction {} has been ABORTED !!!".format(t)) if detailed else None
            elif command == 'W':
                print("--- Transaction {} ---".format(t))
                if not tran.write_element(record):
                    print("!!!Transaction {} has been ABORTED !!!".format(t, record)) if detailed else None
            elif command == 'C':
                if tran.status != 'Aborted':
                    commit_table(self)
                    print("### Transaction {} successfully validated and COMMITED ###".format(t))
        print('------------------------------------------------------------------------------') if detailed else None