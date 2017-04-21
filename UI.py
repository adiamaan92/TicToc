from Tkinter import *


class Application(Frame):

    def say_hi(self):
        print("Simulate Clicked!")

    def createWidgets(self):

        self.hi_there = Button(self)
        self.hi_there["text"] = "Simulate!"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack()

        self.algo_label = Label(self, text="Algorithms available\n Select one..")
        self.algo_label.pack(side="top", fill='both', expand=True, padx=4, pady=4)

        self.Quit = Button(self)
        self.Quit["text"] = "Quit?"
        self.Quit["fg"] = "red"
        self.Quit["command"] = self.quit

        self.Quit.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


def center_window(width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

root = Tk()
root.title("Concurrency Simulator")
center_window(600, 500)
app = Application(master=root)
app.mainloop()
root.destroy()


