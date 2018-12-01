from Model.Parser import Parser
# import View
from Model.ReadFile import ReadFile
from tkinter import *
import os
import gc

class Controller:
    window = None

    def __init__(self, gu):
        self.files_list = self.set_file_list()

    def start(self, data_path, destination_path, stemmer):
        rf = ReadFile(self, stemmer)
        for file in self.files_list:
            rf.set_reader(data_path, destination_path)
            rf.parse_file(file)
            # del rf
            gc.collect()


    def update_progress(self,prog,time):
        self.window.update_prog_time(prog,time)

    def set_file_list(self):
        files_list = []
        for root, dirs, files in os.walk(
                'C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus'):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        return files_list
