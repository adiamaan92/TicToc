import re


class Tictoc(object):
    def __init__(self, n):
        self.data_list = n[:]
        self.x = 0
        self.y = 0
        self.command_list = list()  # A list of list with transaction object, command, and access object

    # Parses the transaction list and generates the commands in the form of list which is stored in the
    # classes's command_list
    def algo_parser(self, text):
        x_match = re.match(r'X = (\d+)', text[0])
        y_match = re.match(r'Y = (\d+)', text[1])
        self.x = int(x_match.group(1))
        self.y = int(y_match.group(1))
        for i in range(2, len(text)):
            temp_match = re.match(r'(.*)(\d)(\((.*)?\))?', text[i])
            self.command_list.append([int(temp_match.group(2)), temp_match.group(1), temp_match.group(3)])
            # print("dummy")

    # returns a boolean of whether a records with a given check_id is locked
    def is_locked(self, check_id):
        for i in self.data_list:
            if i.check_id == check_id:
                return i.lock

    # locks a record with a given check_id
    def lock(self, check_id):
        for i in self.data_list:
            if i.check_id == check_id:
                i.lock = True

    # Returns the record matching the checking_id
    def get_record(self, check_id):
        for i in self.data_list:
            if i.check_id == check_id:
                return i

    # Validates the transaction
    # Most of the logic of the algorithm is implemented here only
    def validate_transaction(self, transaction):
        # Step 1: Lock all the records in the write set to disable deadlock
        for element in transaction.write_list:
            self.lock(element.check_id)
        # Step 2: Compute the commit Timestamp
        commit_set = transaction.read_list + transaction.write_list
        for element in commit_set:
            if element in transaction.write_list:
                transaction.commit_ts = max(transaction.commit_ts, self.get_record(element.check_id).rts + 1)
            else:
                transaction.commit_ts = max(transaction.commit_ts, element.wts)
        # Step 3: Validate the read set
        for element in transaction.read_list:
            if element.rts < transaction.commit_ts:
                if element.wts != self.get_record(element.check_id).wts or \
                        (self.get_record(element.check_id).rts <= transaction.commit_ts and self.is_locked(
                            element.check_id)
                         and element not in transaction.write_list):
                    transaction.abort()
                    return False
                else:
                    self.get_record(element.check_id).rts = max(transaction.commit_ts,
                                                                self.get_record(element.check_id).rts)
        # Step 4 : Write phase. Write all the transactions to the main data list
        for element in transaction.write_list:
            write_element = self.get_record(element.check_id)
            write_element.set_change(element.change)
            write_element.rts, write_element.wts = transaction.commit_ts, transaction.commit_ts
            write_element.lock = False
        return True

    # Goes line by line of the command and handles the overall logic
    def control_logic(self, T1, T2, text):
        set_time = 1
        self.algo_parser(text)
        for transaction, command, records in self.command_list:
            tran = T1 if transaction == 1 else T2
            tran_test = "T1" if transaction == 1 else "T2"
            record = self.x if records == '(X)' else self.y
            if command == 'READ':
                tran.abort() if self.is_locked(record) else tran.read_element(record, t=set_time)
                set_time += 1
            elif command == 'WRITE':
                tran.abort() if self.is_locked(record) else tran.write_element(record, "Placeholder", t=set_time)
                set_time += 1
            elif command == 'COMMIT':
                set_time += 1
                if self.validate_transaction(tran):
                    print("Transaction {} successfully validated and COMMITED".format(tran_test))
                else:
                    print("Transaction {} has been ABORTED".format(tran_test))
