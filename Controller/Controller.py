from Model.ReadFile import ReadFile
from Model.Indexer import Indexer
import pickle
import os
import time
import json

########################################################################################################################
# Class Controller:                                                                                                    #
#                                                                                                                      #
# Listens to actions being made in the GUI by the user and calls the appropriate function in the MODEL                 #
########################################################################################################################


class Controller:
    data_path = ""
    post_path = ""


    def __init__(self, vocab):
        self.vocabulary = vocab
        self.indx = None
        self.total_time = 0
        self.unique_terms = 0
        self.vocabulary_display_mode = None
        self.capital_cities = {}
        self.doc_counter = 0

    def start(self, data_path, post_path, stemmer):
        start = time.time()
        self.data_path = data_path
        self.post_path = post_path
        if not os.path.exists(self.post_path + '/Engine_Data'):
            os.makedirs(self.post_path + '/Engine_Data')
        if not os.path.exists(self.post_path + '/Engine_Data/temp_hash_objects'):
            os.makedirs(self.post_path + '/Engine_Data/temp_hash_objects')
        if not os.path.exists(self.post_path + '/Engine_Data/Vocabulary'):
            os.makedirs(self.post_path + '/Engine_Data/Vocabulary')
        if not os.path.exists(self.post_path + '/Engine_Data/Cities_hash_objects'):
            os.makedirs(self.post_path + '/Engine_Data/Cities_hash_objects')
        if not os.path.exists(self.post_path + '/Engine_Data/posting_files'):
            os.makedirs(self.post_path + '/Engine_Data/posting_files')
        rf = ReadFile(data_path, post_path, stemmer, self)
        rf.start_evaluating()
        self.create_vocabulary()
        self.update_vocabulary_pointers()
        self.create_city_index()
        self.unique_terms = len(self.vocabulary)
        self.indx = Indexer(post_path,self.doc_counter)
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
                del file_hash_terms['#doc_number']
            for key in file_hash_terms:
                if key not in self.vocabulary:
                    self.vocabulary[key] = file_hash_terms[key]['tf_c']
                else:
                    self.vocabulary[key] = self.vocabulary[key] + file_hash_terms[key]['tf_c']
            hash_file.close()
            file_hash_terms = {}
        with open(self.post_path + '\\Engine_Data\\Vocabulary\\Vocabulary.pkl', 'wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)

    def update_vocabulary_pointers(self):
        posting_line_counter = 0
        prev_file = ''
        current_file = ''
        index = 0
        tf = 0
        vocab = self.vocabulary
        vocab = sorted(vocab.items(), key=lambda x: x[0].lower())
        for key, value in vocab:
            if key != '':
                ch = key[0]
                ch_int = ord(key[0])
                tf = self.vocabulary[key]
                if ch.isdigit() or ch == '$':  # numbers
                    current_file = 'num'
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['num', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'num'
                elif 97 <= ch_int <= 98 or 65 <= ch_int <= 66:  # ab
                    current_file = 'ab'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['ab', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'ab'
                elif 99 <= ch_int <= 100 or 67 <= ch_int <= 68:  # cd
                    current_file = 'cd'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['cd', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'cd'
                elif 101 <= ch_int <= 102 or 69 <= ch_int <= 70:  # ef
                    current_file = 'ef'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['ef', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'ef'
                elif 103 <= ch_int <= 104 or 71 <= ch_int <= 72:  # gh
                    current_file = 'gh'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['gh', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'gh'
                elif 105 <= ch_int <= 107 or 73 <= ch_int <= 75:  # ijk
                    current_file = 'ijk'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['ijk', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'ijk'
                elif 108 <= ch_int <= 110 or 76 <= ch_int <= 78:  # lmn
                    current_file = 'lmn'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['lmn', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'lmn'
                elif 111 <= ch_int <= 113 or 79 <= ch_int <= 81:  # opq
                    current_file = 'opq'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['opq', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'opq'
                elif 114 <= ch_int <= 115 or 82 <= ch_int <= 83:  # rs
                    current_file = 'rs'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['rs', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'rs'
                elif 116 <= ch_int <= 118 or 84 <= ch_int <= 86:  # tuv
                    current_file = 'tuv'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['tuv', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'tuv'
                elif 119 <= ch_int <= 122 or 87 <= ch_int <= 90:  # wxy
                    current_file = 'wxy'
                    if current_file != prev_file:
                        posting_line_counter = 0
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['wxy', str(posting_line_counter)]
                    posting_line_counter += 1
                    prev_file = 'wxy'
                else:
                    vocab[index] = (key, tf)
                    self.vocabulary[key] = ['!', str(posting_line_counter)]
                    posting_line_counter += 1
            index += 1
            if posting_line_counter% 1000 == 0:
                print('\n'*100)
                print("Sorting Vocabulary, in line:" + str(posting_line_counter))
        self.vocabulary_display_mode = vocab
        with open(self.post_path + '\\Engine_Data\\Vocabulary\\Vocabulary_with_pointers.pkl', 'wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)
        with open(self.post_path + '\\Engine_Data\\Vocabulary\\Vocabulary_Disp_Mode.pkl', 'wb') as output:
            pickle.dump(vocab, output, pickle.HIGHEST_PROTOCOL)

    def create_city_index(self):
        file_list = self.set_file_list(self.post_path + '/Engine_Data/Cities_hash_objects')
        path = './resources/cities_data.pkl'
        with open(path, 'rb') as data:
            cities_data = pickle.load(data)
        for city_file in file_list:
            with open(city_file, 'rb') as file:
                file_hash_cities = pickle.load(file)
            for key in file_hash_cities:
                if key not in self.capital_cities:
                    if key in cities_data:
                        self.capital_cities[key] = {'Data': '', 'Docs': ''}
                        self.capital_cities[key].update({'Data': cities_data[key], 'Docs': file_hash_cities[key]})
                else:
                    self.capital_cities[key]['Docs'].update(file_hash_cities[key])
        cities_data ={}
        with open(self.post_path + "/Engine_Data/posting_files/cities_index.txt", 'w') as file:
            file.write(json.dumps(self.capital_cities))

    def set_file_list(self, path):
        files_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        # files_list_tmp = []
        # for i in range(5):
        #     files_list_tmp.append(files_list[i])
        # files_list = files_list_tmp
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
