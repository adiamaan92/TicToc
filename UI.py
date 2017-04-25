import tkinter

from tkinter import *

# Application class
class Application(Frame):
    def say_hi(self):
        print("Simulate Clicked!")

    def create_widgets(self):
        self.hi_there = Button(self)
        # self.hi_there["text"] = "Simulate!"
        # self.hi_there["command"] = self.say_hi
        topFrame = Frame(root)
        topFrame.pack()
        bottomFrame = Frame(root)
        bottomFrame.pack(side=BOTTOM)
        self.button1 = Button(bottomFrame, text="simulate", fg="black", bg="green")
        self.button1.pack(side=BOTTOM)
        # on left clicking simulate execute the function name specified in the parameter
        # button1.bind("<Button-1", function name)
        #transaction entry box
        self.label1 = Label(self, text="Please Enter transaction in the given box")
        self.entrybox = Entry(self)
        self.hi_there.pack()
        self.algo_label = Label(self, text="Algorithms available\n Select one..")
        self.algo_label.pack(side="left", fill='both', expand=True, padx=4, pady=4)

        self.c1 = Checkbutton(self, text="TicToc")
        self.c1.pack(side="left")



        self.Quit = Button(self)
        self.Quit["text"] = "Quit?"
        self.Quit["fg"] = "red"
        self.Quit["command"] = self.quit
        self.Quit.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()


def center_window(width=300, height=200):
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
center_window(600, 500)
app = Application(master=root)
#continuously run window
app.mainloop()

root.destroy()
