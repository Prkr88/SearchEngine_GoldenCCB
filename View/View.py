from Controller import Controller
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory


class View:

    def __init__(self, controller):
        self.controller = controller
