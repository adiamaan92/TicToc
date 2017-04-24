class Transaction(object):
    def __init__(self, data_list):
        self.data_list = data_list[:]

    def read_element(self, check_id):
        for i in self.data_list:
            if i.check_id == check_id:
                return i

    def write_element(self, check_id, change):
        for i in self.data_list:
            if i.check_id == check_id:
                i.setchange(change)


