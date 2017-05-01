from Tkinter import *
#import main


class Application(Frame):

    def create_widgets(self):

        self.algo_label.grid(row=0, column=0, columnspan=2, sticky=W)
        self.tictoc.grid(row=1, column=0, columnspan=2, sticky=W)
        self.to.grid(row=2, column=0, columnspan=2, sticky=W)

        self.label1.grid(row=0, column=2, columnspan=2, sticky=W + E + N + S, )
        self.entry_box.grid(row=1, column=2, columnspan=2, sticky=W + E + N + S)

        self.scroll.grid(row=1, column=4, columnspan=1, sticky=W + E + N + S)
        self.entry_box['yscrollcommand'] = "scroll.set"
        self.submit.grid(row=2, column=2, columnspan=2, sticky=W + E + N + S)

        self.bench_marks.grid(row=0, column=5, columnspan=2, sticky=E)
        self.tpcc.grid(row=1, column=4, columnspan=2, sticky=E)
        self.ycsb.grid(row=2, column=4, columnspan=2, sticky=E)

        #self.submit.bind("<Button-1", main.central_logic())

        self.quit.grid(row=3, column=2, columnspan=2, sticky=W + E + N + S)

    def __init__(self, master=None):


        self.frame = Frame(master)
        self.quit = Button(self, text='Exit application', fg="red", bg="black", command=self.quit)
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        #self.frame.grid(row=0, column=0, sticky=N + S + E + W)
        grid = Frame(self.frame)
        grid.grid(sticky=N + S + E + W, column=0, row=7, columnspan=2)
        Grid.rowconfigure(self.frame, 7, weight=1)
        Grid.columnconfigure(self.frame, 0, weight=1)
        # self.width = width
        # self.height = height

        self.tpcc = Checkbutton(self, text="TPC-C")
        self.ycsb = Checkbutton(self, text="YCSB")

        self.bench_marks = Label(self, text="Please select one Benchmark tool")

        self.submit = Button(self, text="simulate", fg="black", bg="green")
        self.entry_box = Text(self, width=35, height=10, wrap=WORD)
        self.scroll = Scrollbar(self, orient="vertical", command=self.entry_box.yview)

        self.label1 = Label(self, text="Please Enter transaction in the given box")
        self.user_text = StringVar()

        self.to = Checkbutton(self, text="TO.py")
        self.tictoc = Checkbutton(self, text="TicToc")
        self.algo_label = Label(self, text="Please select one algorithm")

        self.grid()
        self.create_widgets()


class buildUI(object):

    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Concurrency Simulator")
        self.root.configure(background="white")
        self.width = width
        self.height = height
        self.start()

    def start(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        self.frame = Frame(self.root)
        #self.quit = Button(self, text='Exit application', fg="red", bg="black", command=self.quit)
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        # self.frame.grid(row=0, column=0, sticky=N + S + E + W)
        grid = Frame(self.frame)
        grid.grid(sticky=N + S + E + W, column=0, row=7, columnspan=2)
        Grid.rowconfigure(self.frame, 7, weight=1)
        Grid.columnconfigure(self.frame, 0, weight=1)
        # self.width = width
        # self.height = height

        self.tpcc = Checkbutton(self, text="TPC-C")
        self.ycsb = Checkbutton(self, text="YCSB")

        self.bench_marks = Label(self, text="Please select one Benchmark tool")

        self.submit = Button(self, text="simulate", fg="black", bg="green")
        self.entry_box = Text(self, width=35, height=10, wrap=WORD)
        self.scroll = Scrollbar(self, orient="vertical", command=self.entry_box.yview)

        self.label1 = Label(self, text="Please Enter transaction in the given box")
        self.user_text = StringVar()

        self.to = Checkbutton(self, text="TO.py")
        self.tictoc = Checkbutton(self, text="TicToc")
        self.algo_label = Label(self, text="Please select one algorithm")

        self.grid()
        self.create_widgets()
        self.root.destroy()





