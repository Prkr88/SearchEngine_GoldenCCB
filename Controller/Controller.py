from Model.Parser import Parser
# import View
from Model.ReadFile import ReadFile
from tkinter import *
from Model.Indexer import Indexer
import pickle
import os


# indx = Indexer('C:\\Users\\edoli\\Desktop\\SE_PA')
# indx = Indexer('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine')


class Controller:

    data_path = ""
    post_path = ""
    doc_counter = 0
    def __init__(self, vocab):
        self.vocabulary = vocab
        self.indx = None

    def start(self, data_path, post_path, stemmer):
        self.data_path = data_path
        self.post_path = post_path
        self.indx = Indexer(post_path)
        if not os.path.exists(self.post_path + '/Engine_Data'):
            os.makedirs(self.post_path + '/Engine_Data')
        if not os.path.exists(self.post_path +'/Engine_Data/temp_hash_objects'):
            os.makedirs(self.post_path +'/Engine_Data/temp_hash_objects')
        if not os.path.exists(self.post_path +'/Engine_Data/Vocabulary'):
            os.makedirs(self.post_path +'/Engine_Data/Vocabulary')
        if not os.path.exists(self.post_path +'/Engine_Data/Cities_hash_objects'):
            os.makedirs(self.post_path +'/Engine_Data/Cities_hash_objects')
        rf = ReadFile(data_path, post_path, stemmer, self)
        rf.start_evaluating()
        self.create_vocabulary()
        #self.indx.start_indexing()

    def create_vocabulary(self):
        counter = 0
        file_list = self.set_file_list(self.post_path + '\\Engine_Data\\temp_hash_objects')
        number_of_files = len(file_list)
        for file in file_list:
            with open(file, 'rb') as hash_file:
                counter += 1
                if counter % 20 == 0:
                    p_c = float(counter)
                    p_c = int(p_c * 100 / number_of_files)
                    self.print_prog(p_c)
                file_hash_terms = pickle.load(hash_file)
                self.doc_counter = self.doc_counter + file_hash_terms['#doc_number']
                file_hash_terms.pop('#doc_number', None)
            for key in file_hash_terms:
                if key not in self.vocabulary:
                    self.vocabulary[key] = 0
            hash_file.close()
            file_hash_terms = {}
        with open(self.post_path+'\\Engine_Data\\Vocabulary\\Vocabulary.pkl','wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)
        print(self.doc_counter)

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
        print('Creating Vocabulary:\n[' + '*'*int(p_c/2) + ' '*int((100-p_c)/2) +str(p_c) + '%' ']')

    def reset_system(self):
        if self.indx !=  None:
            self.indx.reset_posting_files()
            self.indx = None
            return 1
        else:
            return None
