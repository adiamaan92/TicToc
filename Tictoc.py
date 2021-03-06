from Queries import commit_table


class Tictoc(object):
    def __init__(self, n):
        self.data_list = n[:]

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

    # Goes line by line of the command and handles the overall logic.
    def control_logic(self, trans_dict, arg_list, command_list, detailed=True):
        set_time = 1
        print('------------------------------------------------------------------------------') if detailed else None
        for command, transaction, records in command_list:
            t = "T" + str(transaction)
            tran = trans_dict[t]
            record = arg_list[records] if records is not None else None
            if command == 'R':
                tran.abort() if self.is_locked(record) else tran.read_element(set_time, record)
                print("     Transaction {} has read {}th record".format(t, record)) if detailed else None
                set_time += 1
            elif command == 'W':
                print("--- Transaction {} ---".format(t)) if detailed else None
                tran.abort() if self.is_locked(record) else tran.write_element(record, set_time)
                print("     Transaction {} has written {}th record locally".format(t, record)) if detailed else None
                set_time += 1
            elif command == 'C':
                set_time += 1
                if self.validate_transaction(tran):
                    commit_table(tran)
                    print("### Transaction {} successfully validated and COMMITED ###".format(t)) if detailed else None
                else:
                    print("!!! Transaction {} has been ABORTED !!!".format(t)) if detailed else None
        print('------------------------------------------------------------------------------') if detailed else None
