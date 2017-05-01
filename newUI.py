from tkinter import *
import copy
import re

from Queries import populate_user
from Tictoc import Tictoc
from TO import TimeStamp
from Transaction import Transaction_TS
from Transaction import Transaction_TicToc

Tran_dict = dict()
arg_list = dict()
command_list = list()
no_of_transactions = 0
set_time = 0
user_list = populate_user(100, db=True)


def buildUI(width, height):

    root = Tk()
    frame = Frame(root)
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    frame.grid(row=0, column=0, sticky=N + S + E + W)
    grid = Frame(frame)
    grid.grid(sticky='W', columnspan=2)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    tpcc_var = IntVar()
    tpcc = Checkbutton(frame, text="TPC-C", variable=tpcc_var)
    tpcc.config(font=("Arial", 11))
    ycsb_var = IntVar()
    ycsb = Checkbutton(frame, text="YCSB", variable=ycsb_var)
    ycsb.config(font=("Arial", 11))

    bench_marks = Label(frame, text="Benchmark tool")
    bench_marks.config(font=("Arial", 11))
    entry_box = Text(frame, width=35, height=10, wrap=WORD)
    scroll = Scrollbar(frame, orient="vertical", command=entry_box.yview)

    label1 = Label(frame, text="Please Enter transaction in the given box")
    user_text = StringVar()

    label1.config(font=("Arial", 11))

    to_var = IntVar()
    to = Checkbutton(frame, text="TO", variable=to_var)
    to.config(font=("Arial", 11))
    tictoc_var = IntVar()
    tictoc = Checkbutton(frame, text="TicToc", variable=tictoc_var)
    tictoc.config(font=("Arial", 11))
    algo_label = Label(frame, text="Concurrency Algorithms")

    algo_label.grid(row=0, column=0, sticky=W + E + S)
    tictoc.grid(row=1, column=0, sticky=W + E + N + S)
    to.grid(row=2, column=0, sticky=W + E + N)

    algo_label.config(font=("Arial", 11))
    label1.grid(row=0, column=2, columnspan=2, sticky=W + E + N + S)
    entry_box.grid(row=1, column=2, columnspan=2, sticky=W + E + N + S)

    submit = Button(frame, text="Simulate", fg="black", bg="green",
                    command=lambda: central_logic(tpcc_var.get(), ycsb_var.get(),
                                                  tictoc_var.get(), to_var.get(), entry_box.get("1.0", END)))
    submit.config(font=("Arial", 11))

    scroll.grid(row=1, column=4, columnspan=1, sticky=W + E + N + S)
    entry_box['yscrollcommand'] = "scroll.set"
    submit.grid(row=2, column=2, columnspan=2, sticky=W + E + N + S)

    bench_marks.grid(row=0, column=5, columnspan=2, sticky=W + E + S)
    tpcc.grid(row=1, column=4, columnspan=2, sticky=W + E + N + S)
    ycsb.grid(row=2, column=4, columnspan=2, sticky=W + E + N + S)

    for x in [0, 2, 5]:
        Grid.columnconfigure(frame, x, weight=1)

    for y in [0, 1]:
        Grid.rowconfigure(frame, y, weight=1)

    root.mainloop()


def central_logic(tpcc_var, ycsb_var, tictoc_var, to_var, entry_box):
    global algorithm
    temp_list = copy.deepcopy(user_list)
    if to_var == 1 and tictoc_var == 0:
        algorithm = TimeStamp(temp_list)
    if to_var == 0 and tictoc_var == 1:
        algorithm = Tictoc(temp_list)
    algo_parser(entry_box.splitlines(), tictoc_var, to_var)
    algorithm.control_logic(Tran_dict, arg_list, command_list)


def initiate_to(trx_list, to_var):
    global set_time
    set_time = 0
    if to_var == 1:
        for i in trx_list:
            set_time += 1
            key = "T" + str(i)
            Tran_dict[key] = Transaction_TS(set_time, algorithm)


def initiate_tictoc(no_transactions, tictoc_var):
    if tictoc_var == 1:
        for i in range(1, no_transactions + 1):
            key = "T" + str(i)
            Tran_dict[key] = Transaction_TicToc(copy.deepcopy(user_list))


def algo_parser(text, tictoc_var, to_var,):
    global no_transactions, command_list, arg_list, Tran_dict
    command_list, arg_list, Tran_dict = list(), dict(), dict()
    for i in text:
        if re.match(r'^T\d+,', i):
            trx_list = re.findall(r'T(\d+)', i)
            initiate_to(trx_list, to_var)
        elif re.match(r'T\s=\s\d+', i):
            trx_match = re.match(r'T\s=\s(\d+)', i)
            no_transactions = int(trx_match.group(1))
            initiate_tictoc(no_transactions, tictoc_var)
        elif re.match(r'^.\s=\s\d+$', i):
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

buildUI(900, 300)