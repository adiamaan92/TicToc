import re


class Tictoc(object):
    def __init__(self, n):
        self.user_list = n[:]
        self.read_list = list()
        self.write_list = list()
        self.x = 0
        self.y = 0
        self.command_list = list()  # A list of list with transaction object, command, and access object

    def algo_parser(self, text):
        x_match = re.match(r'X = (\d+)', text[0])
        y_match = re.match(r'Y = (\d+)', text[1])
        self.x = int(x_match.group(1))
        self.y = int(y_match.group(1))
        for i in range(2, len(text)):
            temp_match = re.match(r'(.*)(\d)(\((.*)?\))?', text[i])
            self.command_list.append([temp_match.group(2), temp_match.group(1), temp_match.group(3)])
        # print("dummy")

    def read_phase(self):
        pass


    def control_logic(self, T1, T2, text):
        self.read_phase()
