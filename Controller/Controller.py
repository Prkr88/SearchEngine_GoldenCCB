from Model.Parser import Parser
# import View
from Model.ReadFile import ReadFile
from tkinter import *
from Model.Indexer import Indexer
import pickle
import os

class Controller:

    data_path = ""
    post_path = ""
    def __init__(self, vocab):
        self.vocabulary = vocab

    def start(self, data_path, post_path, stemmer):
        self.data_path = data_path
        self.post_path = post_path
        if not os.path.exists(self.post_path + '/Engine_Data'):
            os.makedirs(self.post_path + '/Engine_Data')
        if not os.path.exists(self.post_path +'/Engine_Data/temp_hash_objects'):
            os.makedirs(self.post_path +'/Engine_Data/temp_hash_objects')
        if not os.path.exists(self.post_path +'/Engine_Data/Vocabulary'):
            os.makedirs(self.post_path +'/Engine_Data/Vocabulary')
        rf = ReadFile(data_path, post_path, stemmer, self)
        rf.start_evaluating()
        self.create_vocabulary()
        #indx = Indexer('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine')
        #indx.start_indexing()

    def create_vocabulary(self):
        counter = 0
        file_list = self.set_file_list(self.post_path + '\\Engine_Data\\temp_hash_objects')
        for file in file_list:
            with open(file, 'rb') as hash_file:
                counter += 1
                if counter % 20 == 0:
                    p_c = float(counter)
                    p_c = int(p_c * 100 / 1815)
                    self.print_prog(p_c)
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key not in self.vocabulary:
                    self.vocabulary[key] = 0
            hash_file.close()
            file_hash_terms = {}
        with open(self.post_path+'\\Engine_Data\\Vocabulary\\Vocabulary.pkl','wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)

    def set_file_list(self, path):
        files_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        # files_list_tmp = []
        # for i in range(20):
        #     files_list_tmp.append(files_list[i])
        return files_list

    def print_prog(self, p_c):
        print('\n'*100)
        print('Creating Vocabulary:[' + '*'*p_c + ' '*(100-p_c) +str(p_c) + '%' ']')