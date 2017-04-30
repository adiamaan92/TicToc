# All the tables are created as a class here. It will have two extra fields check_id and change
# All tables in the database should have a relevant data structure created like this
# It can have any number of fields,  but check_id and change are the important fields
# check_id is the primary key in a table and change is the field that you want to change
# only the check_id can be used to access the records and the change is the only field that
# can be changed during the process


class User(object):
    def __init__(self, user_id, name, age, wts=0, rts=0):
        self.user_id = user_id
        self.check_id = self.user_id
        self.name = name
        self.age = age
        self.wts = wts
        self.rts = rts
        self.lock = False
        self.change = self.name

    # Atomic operation to make sure both the fields change at once
    def set_change(self, change):
        self.name, self.change = change, change


# class Account(object):
#     def __init__(self, user_id, name, age, wts=0, rts=0):
#         self.user_id = user_id
#         self.check_id = self.user_id
#         self.name = name
#         self.age = age
#         self.wts = wts
#         self.rts = rts
#         self.lock = False
#         self.change = self.name
#
#     # Atomic operation to make sure both the fields change at once
#     def set_change(self, change):
#         self.name, self.change = change, change
