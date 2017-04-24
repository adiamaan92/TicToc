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

    def setchange(self, change):
        self.name = self.change
        self.change = change




