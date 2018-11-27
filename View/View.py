from Controller import Controller
from tkinter import *
from tkinter import font
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import os
from tkinter import font as tkfont


dir = os.getcwd()  # current working directory


class View:

    # init new Master window
    def __init__(self, controller, root):
        self.controller = controller
        master = root
        master.title("Golden CCB Search Engine")
        master.resizable(0, 0)
        master.wm_attributes('-transparentcolor', 'gainsboro')

        # self.main_window = Frame(master)
        # self.main_window.pack()
        # cv = Canvas(self.main_window, width=w, height=h)

        bg_image = tk.PhotoImage(file=dir + '\\resources\\bg.png')
        w = bg_image.width()  # get the width and height of the image
        h = bg_image.height()
        cv = tk.Canvas(master, width=w, height=h)

        self.main_window = tk.Frame(cv)
        cv.pack(side="left", fill="both", expand=True)
        cv.create_window((4,4), window=self.main_window, anchor="nw", tags="self.main_window")

        # cv.pack(side='top', fill='both', expand='yes')
        cv.create_image(0, 0, image=bg_image, anchor='nw')

        # MainWindow = cv.create_window(10, 10, window=master, anchor='nw')


        BTN_WIDTH = 30
        BTN_HEIGHT = 2
        ENTRY_WIDTH = 50
        ENTRY_HEIGHT = 2

        bold = tkfont.Font(family="Helvetica", size=12, weight="bold")
        BTN_FONT_SIZE = 8

        button_width = BTN_WIDTH
        button_height = BTN_HEIGHT
        self.fontSize = BTN_FONT_SIZE

        text_canvas1 = cv.create_text(128, 140, anchor="nw", fill='white', font=bold)
        cv.itemconfig(text_canvas1, text="Corpus Path:")

        button1 = Button(text="Browse", anchor=W, cursor='hand2', bg='white', highlightcolor='pink', relief='raised', state='active')
        button1.configure(width=5, relief=FLAT)
        button1_window = cv.create_window(670, 150, window=button1, height=18, width=50)

        text_canvas2 = cv.create_text(100, 180, anchor="nw", fill='white', font=bold)
        cv.itemconfig(text_canvas2, text="Stopwords Path:")

        button2 = Button(text="Browse", anchor=W, cursor='hand2', bg='white', highlightcolor='pink', relief='raised', state='active')
        button2.configure(width=5, relief=FLAT)
        button2_window = cv.create_window(670, 190, window=button2, height=18, width=50)

        e1 = Entry(cv)
        cv.create_window(430, 150, window=e1, height=18, width=400)
        e2 = Entry(cv)
        cv.create_window(430, 190, window=e2, height=18, width=400)

        text_canvas3 = cv.create_text(155, 220, anchor="nw", fill='white', font=bold)
        cv.itemconfig(text_canvas3, text="Stemmer:")
        CheckVar1 = IntVar()
        c1 = Checkbutton(master, variable=CheckVar1, onvalue=1, offvalue=0, height=20, width=4)
        cv.create_window(240, 230, window=c1, height=16, width=15)

        logo_file = "resources\\GoldenCCB_logo.png"
        logo_photo = Image.open(logo_file)
        logo_photo_size = logo_photo.resize((150, 160), Image.ANTIALIAS, )
        tk_logo = ImageTk.PhotoImage(logo_photo_size)
        cv.create_image(410, 85, image=tk_logo)

        # self.logo_label = self.__set_logo()
        # self.data_label.pack(side='left', padx=10, pady=5, anchor='sw')
        # self.data_label = Label(self.main_window, relief=FLAT, fg='white', text='Corpus Path:')
        # self.data_label.grid(row=10, column=3)
        # self.data_path_entry = self.__set_data_path_entry(self.main_window, 1, 1, ENTRY_WIDTH)

        # self.data_browse_BTN = self.__set_data_browse_BTN(self.main_window, self.__set_browse, 1, 2, button_width,
        #                                               button_height)
        # self.stop_words_label = Label(self.main_window, relief=FLAT, bg='white', text='Stopwords Path:')
        # self.stop_words_label.grid(row=10, column=0, padx=10, pady=10)
        # self.stop_words_entry = self.__set_stop_words_entry(self.main_window, 10, 1, ENTRY_WIDTH)
        # self.stop_words_browse_BTN = self.__set_stop_words_browse_BTN(self.main_window, self.__set_browse, 10, 2, button_width,
        #                                               button_height)

        master.mainloop()

    def show(self):
        """
        # set constants
        BTN_WIDTH = 30
        BTN_HEIGHT = 2
        ENTRY_WIDTH = 50
        ENTRY_HEIGHT = 2
        BTN_FONT_SIZE = 8
        button_width = BTN_WIDTH
        button_height = BTN_HEIGHT
        self.fontSize = BTN_FONT_SIZE

        self.main_window = Frame(self.master)
        self.main_window.pack()
        self.logo_label = self.__set_logo()
        self.data_label = Label(self.main_window, relief=FLAT, bg='white', text='Data Path:')
        self.data_label.grid(row=1, column=0)
        self.data_path_entry = self.__set_data_path_entry(self.main_window, 1, 1, ENTRY_WIDTH)
        self.data_browse_BTN = self.__set_data_browse_BTN(self.main_window, self.__set_browse, 1, 2, button_width,
                                                       button_height)
        self.stop_words_label = Label(self.main_window, relief=FLAT, bg='white', text='Stopwords Path:')
        self.stop_words_label.grid(row=10, column=0, padx=10, pady=10)
        self.stop_words_entry = self.__set_stop_words_entry(self.main_window, 10, 1, ENTRY_WIDTH)
        self.stop_words_browse_BTN = self.__set_stop_words_browse_BTN(self.main_window, self.__set_browse, 10, 2, button_width,
                                                       button_height)

        # The status bar at the bottom of the frame
        # self.statusBar = Frame(self.master, bg="white", relief=SUNKEN, height="50", width=(button_width * 2))
        # self.statusBar.pack(side=BOTTOM, fill=X)
        """

    def __set_data_browse_BTN(self, main_window, func, row, col, button_width, button_height):
        browse_data_button = Button(main_window, text="Browse", width=5, height=1,
                                    font=('times', self.fontSize, 'bold'), command=func, fg='white', activebackground='gold')
        browse_data_button.grid(row=row, column=col)
        return browse_data_button

    def __set_data_path_entry(self, main_window, row, col, w):
        data_path_entry = Entry(main_window, text="insert path", width=w, bg='white')
        # data_path_entry.pack(side='left', padx=row, pady=col, anchor='sw')
        data_path_entry.grid(row=row, column=col)
        return data_path_entry

    def __set_stop_words_browse_BTN(self, main_window, func, row, col, button_width, button_height):
        browse_stop_words_button = Button(main_window, text="Browse", width=5, height=1,
                                    font=('times', self.fontSize, 'bold'), command=func, fg='white', activebackground='gold')
        browse_stop_words_button.grid(row=row, column=col)
        return browse_stop_words_button

    def __set_stop_words_entry(self, main_window, row, col, w):
        stop_words_entry = Entry(main_window, text="insert path", width=w, bg='white')
        stop_words_entry.grid(row=row, column=col)
        return stop_words_entry

    def __set_logo(self):
        logo_file = "resources\\GoldenCCB_logo.png"
        logo_photo = Image.open(logo_file)
        logo_photo_size = logo_photo.resize((200, 200), Image.ANTIALIAS, )
        tk_logo = ImageTk.PhotoImage(logo_photo_size)
        logo_label = Label(self.cv, image=tk_logo)
        logo_label.image = tk_logo
        # logo_label.grid(row=0, column=0, columnspan=3, rowspan=1, sticky=W + E + N + S, padx=5, pady=5)
        return logo_label


    def __set_browse(self):
        print('fuck')
