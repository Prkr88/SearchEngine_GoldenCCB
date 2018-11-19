from Model.Parser import Parser
from View.View import View
from tkinter import *


class Controller:

    def __init__(self):
        self.root = Tk()
        self.view = View(self.root, self)

    def start(self):
        print('start')
        self.root.resizable(0, 0)
        self.root.mainloop()
