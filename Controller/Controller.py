from Model.Parser import Parser
# import View
from Model.ReadFile import ReadFile
from tkinter import *
from Model.Indexer import Indexer

class Controller:
    window = None

    def __init__(self, gu):
        #self.window = window
        self.Gu = None

    def start(self, data_path, destination_path, stemmer):
        rf = ReadFile(data_path, destination_path, stemmer, self)
        rf.start_evaluating()
        print("Done Parsing")
        #indx = Indexer('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine')
        #indx.start_indexing()

    def update_progress(self,prog,time):
        self.window.update_prog_time(prog,time)
