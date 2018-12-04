from Model.Parser import Parser
# import View
from Model.ReadFile import ReadFile
from tkinter import *
from Model.Indexer import Indexer
import pickle
import os
import time


# indx = Indexer('C:\\Users\\edoli\\Desktop\\SE_PA')
# indx = Indexer('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine')


class Controller:
    data_path = ""
    post_path = ""
    doc_counter = 0

    def __init__(self, vocab):
        self.vocabulary = vocab
        self.indx = None
        self.total_time = 0
        self.unique_terms = 0

    def start(self, data_path, post_path, stemmer):
        start = time.time()
        self.data_path = data_path
        self.post_path = post_path
        self.indx = Indexer(post_path)
        if not os.path.exists(self.post_path + '/Engine_Data'):
            os.makedirs(self.post_path + '/Engine_Data')
        if not os.path.exists(self.post_path + '/Engine_Data/temp_hash_objects'):
            os.makedirs(self.post_path + '/Engine_Data/temp_hash_objects')
        if not os.path.exists(self.post_path + '/Engine_Data/Vocabulary'):
            os.makedirs(self.post_path + '/Engine_Data/Vocabulary')
        if not os.path.exists(self.post_path + '/Engine_Data/Cities_hash_objects'):
            os.makedirs(self.post_path + '/Engine_Data/Cities_hash_objects')
        rf = ReadFile(data_path, post_path, stemmer, self)
        rf.start_evaluating()
        self.create_vocabulary()
        #self.update_vocabulary_pointers()
        self.unique_terms = len(self.vocabulary)
        self.indx.start_indexing()
        end = time.time()
        self.total_time = (end - start)

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
        with open(self.post_path + '\\Engine_Data\\Vocabulary\\Vocabulary.pkl', 'wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)

    def update_vocabulary_pointers(self):
        posting_line_counter = 0
        prev_file = ''
        current_file = ''
        vocab = self.vocabulary
        vocab = sorted(vocab.items(), key=lambda x: x[0].lower())
        for key in vocab:
            ch = key[0]
            if ch.isdigit() or ch == '$':  # numbers
                current_file = 'num'
                vocab[key] = ['num', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'num'
            elif 97 <= ch <= 98 or 65 <= ch <= 66:  # ab
                current_file = 'ab'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['ab', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'ab'
            elif 99 <= ch <= 100 or 67 <= ch <= 68:  # cd
                current_file = 'cd'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['cd', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'cd'
            elif 101 <= ch <= 102 or 69 <= ch <= 70:  # ef
                current_file = 'ef'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['ef', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'ef'
            elif 103 <= ch <= 104 or 71 <= ch <= 72:  # gh
                current_file = 'gh'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['gh', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'gh'
            elif 105 <= ch <= 107 or 73 <= ch <= 75:  # ijk
                current_file = 'ijk'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['ijk', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'ijk'
            elif 108 <= ch <= 110 or 76 <= ch <= 78:  # lmn
                current_file = 'lmn'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['lmn', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'lmn'
            elif 111 <= ch <= 113 or 79 <= ch <= 81:  # opq
                current_file = 'opq'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['opq', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'opq'
            elif 114 <= ch <= 115 or 82 <= ch <= 83:  # rs
                current_file = 'rs'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['rs', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'rs'
            elif 116 <= ch <= 118 or 84 <= ch <= 86:  # tuv
                current_file = 'tuv'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['tuv', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'tuv'
            elif 119 <= ch <= 122 or 87 <= ch <= 90:  # wxy
                current_file = 'wxy'
                if current_file != prev_file:
                    posting_line_counter = 0
                vocab[key] = ['wxy', str(posting_line_counter)]
                posting_line_counter += 1
                prev_file = 'wxy'
        with open(self.post_path + '\\Engine_Data\\Vocabulary\\Vocabulary_with_pointers.pkl', 'wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)

    def set_file_list(self, path):
        files_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        files_list_tmp = []
        for i in range(5):
            files_list_tmp.append(files_list[i])
        files_list = files_list_tmp
        return files_list

    def print_prog(self, p_c):
        print('\n' * 100)
        print('Creating Vocabulary:\n[' + '*' * int(p_c / 2) + ' ' * int((100 - p_c) / 2) + str(p_c) + '%' ']')

    def reset_system(self):
        if self.indx != None:
            self.indx.reset_posting_files()
            self.indx = None
            return 1
        else:
            return None
