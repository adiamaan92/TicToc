# This Transaction is specific to TicToc.
# If you are going to implement a different algorithm right its own Transaction
import copy

from Queries import random_name


class Transaction_TicToc(object):
    def __init__(self, data_list):
        self.data_list = data_list[:]
        self.status = "Initialized"
        self.read_list = list()
        self.write_list = list()
        self.commit_ts = 0

    # Reads an element using check id and sets its read time stamp to the present time
    # the element is also added to the write set as well
    def read_element(self, ti, check_id):
        for i in self.data_list:
            if i.check_id == check_id:
                self.read_list.append(i)
                i.rts = ti
                # time.sleep(1)
                break

    # Writes an element using check_id and value is set to change for the change field
    def write_element(self, check_id, ti):
        for i in self.data_list:
            if i.check_id == check_id:
                rname = random_name()
                print("Trying to change the name from {} to {}".format(i.name, rname))
                i.set_change(rname)
                self.write_list.append(i)
                i.wts = ti
                # time.sleep(1)
                break

    # Sets the status of the transaction to aborted
    def abort(self):
        self.status = "Aborted!"


class Transaction_TS(object):
    def __init__(self, TS, TO):
        self.status = "Initialized"
        self.TS = TS
        self.TO = TO

    # Reads an element using check id and sets its read time stamp to the present time
    # the element is also added to the write set as well
    def read_element(self, check_id):
        for i in self.TO.data_list:
            if i.check_id == check_id:
                if i.wts > self.TS:
                    self.abort()
                    print(
                    "     The record {} has been written by a later transaction. Hence aborting read".format(check_id))
                    return False
                else:
                    self.TO.dependent_list.append(i)
                    i.rts = max(i.rts, self.TS)
                    print("     The record {} has been successfully read".format(check_id))
                    return True

    # Writes an element using check_id and value is set to change for the change field
    def write_element(self, check_id):
        for i in self.TO.data_list:
            if i.check_id == check_id:
                if i.rts > self.TS:
                    self.abort()
                    print(
                    "     The record {} has been read by a later transaction. Hence aborting write".format(check_id))
                    return False
                if i.wts > self.TS:
                    pass
                else:
                    self.TO.old_list.append(i)
                    i.wts = self.TS
                    rname = random_name()
                    print("     Trying to change the name from {} to {}".format(i.name, rname))
                    i.set_change(rname)
                    return True

    # Sets the status of the transaction to aborted
    def abort(self):
        self.status = 'Aborted'
        for i in self.TO.old_list:
            for j in self.TO.data_list:
                if i.wts == j.wts:
                    j = copy.deepcopy(i)

    def set_ts(self, ts):
        self.TS = ts
