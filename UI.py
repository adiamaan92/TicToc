import tkinter

from tkinter import *

# Application class
class Application(Frame):

    def create_widgets(self):
                        #LEFT GRID
        # algorithms grid
        self.algo_label = Label(self, text="Please select one algorithm")
        self.algo_label.grid(row=0, column=0, columnspan=2, sticky=W)
        self.c1 = Checkbutton(self, text="TicToc")
        self.c1.grid(row=1, column=0, columnspan=2, sticky=W)
        self.c1 = Checkbutton(self, text="TO")
        self.c1.grid(row=2, column=0, columnspan=2, sticky=W)
               #CENTER GRID
        # to read text entered in the text box
        self.usertext = StringVar()
        #transaction entry box
        self.label1 = Label(self, text="Please Enter transaction in the given box" )
        self.label1.grid(row=0, column=2, columnspan=2, sticky=W+E+N+S,)
        self.entrybox = Text(self, width = 35, height = 10, wrap = WORD)
        self.entrybox.grid(row=1, column=2, columnspan=2, sticky=W+E+N+S)
        #adding scrollbar to the box
        self.scroll = Scrollbar(self, orient="vertical", command=self.entrybox.yview)
        self.scroll.grid(row=1,column=4,columnspan=1, sticky=W+E+N+S)
        self.entrybox['yscrollcommand'] = "scroll.set"
        self.button1 = Button(self, text="simulate", fg="black", bg="green")
        self.button1.grid(row=2, column=2, columnspan=2, sticky=W+E+N+S)
        # on left clicking simulate execute the function name specified in the parameter
        # button1.bind("<Button-1", function name)

            #RIGHT GRID
        #Benchmarks grid
        self.bench_marks = Label(self, text="Please select one Benchmark tool")
        self.bench_marks.grid(row=0, column=5, columnspan=2, sticky=E)

        self.c1 = Checkbutton(self, text="YCSB")
        self.c1.grid(row=1, column=4, columnspan=2, sticky=E)
        self.c2 = Checkbutton(self, text="TPC-C")
        self.c2.grid(row=2, column=4, columnspan=2, sticky=E)


        #Quit button
        self.Quit = Button(self, text='Exit application', fg="red", bg="black", command=self.quit)
        self.Quit.grid(row=3, column=2, columnspan=2, sticky=W+E+N+S)



    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()


def center_window(width=100, height=100):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

#main window
root = Tk()
root.title("Concurrency Simulator")
root.configure(background="yellow")
#center_window(650, 400)
app = Application(master=root)
#continuously run window
app.mainloop()

root.destroy()
