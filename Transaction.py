import time
import copy


class Transaction(object):
    def __init__(self, data_list):
        self.data_list = data_list[:]
        self.status = "Initialized"
        self.read_list = list()
        self.write_list = list()
        self.commit_ts = 0

    # Reads an element using check id and sets its read time stamp to the present time
    # the element is also added to the write set as well
    def read_element(self, check_id, t):
        for i in self.data_list:
            if i.check_id == check_id:
                self.read_list.append(copy.deepcopy(i))
                i.rts = t
                time.sleep(1)
                break

    # Writes an element using check_id and value is set to change for the change field
    def write_element(self, check_id, change, t):
        for i in self.data_list:
            if i.check_id == check_id:
                i.set_change(change)
                self.write_list.append(copy.deepcopy(i))
                i.wts = t
                time.sleep(1)
                break

    # Sets the status of the transaction to aborted
    def abort(self):
        self.status = "Aborted!"
