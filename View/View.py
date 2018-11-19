from Controller import Controller
import tkinter
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askdirectory


class View:

    # init new Master window
    def __init__(self, master, controller):
        self.controller = controller
        # set Constants
        BTN_WIDTH = 30
        BTN_HEIGHT = 2
        ENTRY_WIDTH = 30
        ENTRY_HEIGHT = 2
        BTN_FONT_SIZE = 8

        # set parameters
        button_width = BTN_WIDTH
        button_height = BTN_HEIGHT
        self.fontSize = BTN_FONT_SIZE

        # Main Buttons ##
        master.geometry('500x500')
        self.main_window = Frame(master)
        self.main_window.pack(side=TOP)
        self.logo_label = self.__set_logo()
        self.data_label = Label(self.main_window, text='Data Path:').grid(row=1, column=0)
        self.data_path_entry = self.__set_data_path_entry(self.main_window, 1, 1, ENTRY_WIDTH)
        self.data_browse_BTN = self.__set_data_browse_BTN(self.main_window, self.__set_browse, 1, 2, button_width,
                                                       button_height)


    def __set_data_browse_BTN(self, main_window, func, row, col, button_width, button_height):
        browse_data_button = Button(main_window, text="Browse", width=5, height=1,
                                    font=('times', self.fontSize, 'bold'), command=func, bg='gainsboro')
        browse_data_button.grid(row=row, column=col)
        return browse_data_button

    def __set_data_path_entry(self, main_window, row, col, w):
        data_path_entry = Entry(main_window, text="insert path", width=w, bg='gainsboro')
        data_path_entry.grid(row=row, column=col)
        return data_path_entry

    def __set_logo(self):
        logo_file = "resources\\GoldenCCB_logo.png"
        logo_photo = Image.open(logo_file)
        logo_photo_size = logo_photo.resize((300, 300), Image.ANTIALIAS)
        tk_logo = ImageTk.PhotoImage(logo_photo_size)
        logo_label = Label(self.main_window, image=tk_logo)
        logo_label.image = tk_logo
        logo_label.grid(row=0, column=0, columnspan=3, rowspan=1, sticky=W + E + N + S, padx=5, pady=5)
        return logo_label

    def __set_browse(self):
        print('fuck')