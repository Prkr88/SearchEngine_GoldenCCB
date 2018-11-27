from Model.Parser import Parser
from View.View import View
from tkinter import *


class Controller:

    def __init__(self):
        self.root = Tk()

    def start(self):
        view = View(self, self.root)

