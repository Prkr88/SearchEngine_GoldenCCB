import os
from Model.Parser import Parser
import time
import multiprocessing
import pickle


########################################################################################################################
# Class ReadFile:                                                                                                      #
#                                                                                                                      #
# Receives a Corpus path, stopwords path and a stemming option (from the Controller) and returns temporary pickle files#
# containing dictionaries of tokens                                                                                    #
# - Runs a process pool -                                                                                              #
#                                                                                                                      #
########################################################################################################################


f_counter = None


class ReadFile:
    f_counter = 0
    files_list = []
    complete_list = []
    controller = None
    percent = 0
    stemmer = None
    semaphore = None
    number_of_files = 0
    hash_stopwords = {}
    hash_keywords_months = {}
    hash_keywords_prices = {}
    hash_punc = {}
    hash_punc_middle = {}
    hash_alphabet = {}
    vocabulary = {}
    hash_terms_collection = {}
    data_path = ""
    post_path = ""
    # indexer = Indexer('C:/Users/edoli/Desktop/SE_PA')
    # ('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus'):
    # ('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus\\corpus'):
    # ('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus\\FB396001'):
    # with open('C:\\Users\\edoli\\Desktop\\SE_PA\\temp_hash_objects\\file_hash_'+ p_name+'.pkl' , 'wb') as output:

    # initializes shared variable for the process pool #

    def init_globals(self, f_c):
        global f_counter
        f_counter = f_c

    # constructor #

    def __init__(self, data_path, post_path, stemmer,controller):
        self.data_path = data_path
        self.post_path = post_path
        print('\n' * 100)
        print('Parssing:\n[' + ' ' * 50 + '%0' ']')
        self.controller = controller
        self.stemmer = stemmer

    # function sets stopwords #

    def set_stopwords(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        list_stopwords = data.split()
        for word in list_stopwords:
            self.hash_stopwords[word] = ""
        del list_stopwords

    # function sets month keywords #

    def set_keywords_months(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        list_keywords_months = data.split()
        for word in list_keywords_months:
            self.hash_keywords_months[word] = ""
        del list_keywords_months

    # function sets price keywords #

    def set_keywords_prices(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        list_keywords_prices = data.split()
        for word in list_keywords_prices:
            self.hash_keywords_prices[word] = ""
        del list_keywords_prices

    # function sets punctuation keywords #

    def set_puncwords(self):
        list_punc = {' ', '', "\"", '\"', "\\", '\\\\', ',', '"', '|' '?', '-', '--', '_', '*', '"', '`', ':', '.', '/',
                     ';', "'", '[', ']', '(', ')', '{', "}", '<', '>', '~', '%', '^', '?', '&', '!', "=", '+', "#",
                    '\n', '<P>', '</P>', '<F>', '</F>', '/F', 'MR'}
        for word in list_punc:
            self.hash_punc[word] = ""
        del list_punc

    # function sets alphabetical keywords #

    def set_alphabet(self):
            self.hash_alphabet = {'a': "", 'A': "", 'b': "", 'B': "", 'c': "", 'C': "", 'd': "", 'D': "",
            'e': "", 'E': "", 'f': "", 'F': "", 'g': "", 'G': "", 'h': "", 'H': "",
            'i': "", 'I': "", 'j': "", 'J': "", 'k': "", 'K': "", 'l': "", 'L': "", 'm': "", 'M': "", 'n': "", 'N': "",
            'o': "", 'O': "", 'p': "", 'P': "", 'q': "", 'Q': "", 'r': "", 'R': "", 's': "", 'S': "",
            't': "", 'T': "", 'u': "", 'U': "", 'v': "", 'V': "", 'w': "", 'W': "", 'x': "", 'X': "",
            'y': "", 'Y': "", 'z': "", 'Z': ""}

    # function sets punctuation keywords #

    def set_middlewords(self):
        list_punc = {'.', '/','|', '>', ';', '^', '?', '\"', '!', "=", '+', "#", "\\", '\\\\', '[', ']', '(', ')', '{', "}", ' '}
        for word in list_punc:
            self.hash_punc_middle[word] = ""
        del list_punc

    # function inits paths and dictionaries #

    def init_helpers(self):
        project_dir = os.path.dirname(os.path.dirname(__file__))
        str_path_stopwords = 'resources\\stopwords.txt'  # sets stop word dictionary
        str_path_keywords_months = 'resources\\keywords_months.txt'  # sets key word dictionary
        str_path_keywords_prices = 'resources\\keywords_prices.txt'  # sets key word dictionary
        # str_path_test = 'C:\\Users\\edoli\\Desktop\\SE_PA\\test1.txt'
        # self.set_test_file(str_path_test)
        self.abs_stopword_path = os.path.join(project_dir, str_path_stopwords)
        self.abs_keyword_path_months = os.path.join(project_dir, str_path_keywords_months)
        self.abs_keyword_path_prices = os.path.join(project_dir, str_path_keywords_prices)
        self.set_stopwords(self.abs_stopword_path)  # sets stop word dictionary
        self.set_keywords_months(self.abs_keyword_path_months)  # sets key word dictionary
        self.set_keywords_prices(self.abs_keyword_path_prices)  # sets key word dictionary
        self.set_puncwords()  # sets punctuation vocabulary
        self.set_middlewords()
        self.set_alphabet()
        with open('resources\\cities_data.pkl', 'rb') as input:
            self.hash_cities = pickle.load(input)

    # main function that runs over the given corpus and calls the Parser Class #

    def start_evaluating(self):
        global f_counter
        f_counter = multiprocessing.Value('i', 0)
        files_list = self.set_file_list()
        self.number_of_files = len(files_list)
        # for file in files_list:
        #     self.parse_file(file)
        pool = multiprocessing.Pool(processes=4, initializer=self.init_globals, initargs=(f_counter,))
        i = pool.map_async(self.parse_file, files_list, chunksize=1)
        i.wait()

    # function sets path list of files for the process pool jobs #

    def set_file_list(self):
        files_list = []
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        files_list_tmp = []
        for i in range(100):
             files_list_tmp.append(files_list[i])
        files_list = files_list_tmp
        return files_list

    # main function initializing folders saving data and send documents to the parser #

    def parse_file(self, file_path):
        if len(self.hash_stopwords) == 0:
            self.init_helpers()
        global f_counter
        p = None
        file_terms = {}
        p_name = "#NUM_" + str(f_counter.value)
        with f_counter.get_lock():
           f_counter.value += 1
        f_start = time.time()
        p = Parser(self.hash_stopwords,self.hash_keywords_months,self.hash_keywords_prices,self.hash_punc,self.hash_punc_middle,self.hash_alphabet, self.stemmer)
        self.get_doc_from_file(file_path, p)
        with open(self.post_path + '/Engine_Data/temp_hash_objects/file_hash_'+ p_name+'.pkl', 'wb') as output:
            pickle.dump(p.hash_terms, output, pickle.HIGHEST_PROTOCOL)
        with open(self.post_path + '/Engine_Data/Cities_hash_objects/hash_cities'+ p_name+'.pkl', 'wb') as output:
            pickle.dump(p.hash_cities, output, pickle.HIGHEST_PROTOCOL)
        file_terms = {}
        self.vocabulary = {}
        f_end = time.time()
        time_to_file = f_end - f_start
        if f_counter.value % 20 == 0:
            p_c = float(f_counter.value)
            p_c = int(p_c * 100 / self.number_of_files)
            if p_c != self.percent:
                self.percent = p_c
                self.print_prog(p_c)

    # function tool for displaying the progress bar #

    def print_prog(self, p_c):
        print('\n'*100)
        print('Parssing:\n[' + '*'*int(p_c/2) + ' '*int((100-p_c)/2) +str(p_c) + '%' ']')

    # main function extracting documents from given strings and calls the start_parse(doc) method #

    def get_doc_from_file(self, file_path, parser_object):
        skip_one = 0
        with open(file_path, 'r') as file:
            doc_counter = 0
            doc_counter2 = 0
            data = file.read()
            data_list = data.split("<DOC>")
            del data
            for doc in data_list:
                doc_counter2 += 1
                if skip_one == 1:
                    doc_counter += 1
                    doc = "<DOC>" + doc
                    parser_object.start_pase(doc)
                else:
                    skip_one = 1
        parser_object.hash_terms['#doc_number'] = parser_object.doc_counter
        del data_list

    # function merges the vocabulary #

    def merge_file_terms(self, file_terms):
        global hash_c
        global voc
        global f_counter
        #hash_c.update(file_terms)
        for key, value in file_terms.items():
            vocab = voc
            hash_col = hash_c
            #with f_counter.get_lock():
            if key not in self.vocabulary:
                vocab[key] = 0
                hash_col[key] = value
            else:
                print("edited")
                hash_col[key]['tf_c'] = hash_col[key]['tf_c'] + file_terms[key]['tf_c']
                hash_col[key]['df'] = hash_col[key]['df'] + file_terms[key]['df']
                for d_id in file_terms[key]['hash_docs']:
                    hash_col[key]['hash_docs'].update({d_id: file_terms[key]['hash_docs'][d_id]})
        print("merged")
