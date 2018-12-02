import os
from asyncio import sleep
from Model.Parser import Parser
from Model.Indexer import Indexer
import time
import sys
import gc
import cProfile, pstats
import time
import json
import timeit
from io import StringIO
import multiprocessing
from multiprocessing import Pool, Lock, Manager, Array
from Model.API import API
import pickle

# ('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus'):
# ('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus\\corpus'):
# ('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus\\FB396001'):
# ('C:\\Users\\edoli\\Desktop\\SE_PA')

'''
# <F P=104>  Rotterdam NRC HANDELSBLAD </F>
str_doc = """ <DOC><DOCNO> FBIS3-1 </DOCNO><HT>  "cr00000011094001" </HT><HEADER><H2> <F P=104>  Beijing GUANGMING RIBAO </F>   March Reports </H2><DATE1>  1 March 1994 </DATE1>Article Type:FBIS Document Type:FOREIGN MEDIA NOTE--FB PN 94-028 <H3> <TI>      FORMER YUGOSLAV REPUBLIC OF MACEDONIA: OPINION POLLS ON </TI></H3></HEADER><TEXT>matan@gmail.com U.S. edo@gmail.com Summary:  Newspapers in the Former Yugoslav Republic of    Macedonia have published the results of opinion polls,    indicating the relative popularity of politicians,    political parties, and attitudes toward the political system.    The 22-23 January edition of the Skopje newspaper VECER in Macedonian published on pages 6-7 the results of an opinion poll conducted by the "BriMa" agency in November 1993. According to VECER, 1,036 respondents were classified by age and residence, but the paper did not explain the methodology or give the margin of error.  For the purpose of comparison, the paper cited the results of an unidentified poll made in May 1993. The approval/disapproval ratings, in percent, for ten Macedonian politicians were:                                            November 1993    May 1993 Kiro Gligorov, President of the Republic      76/15           78/13 Vasil Tupurkovski, former Macedonian          50/36           43/37    official in Federal Yugoslavia Ljubomir Frckovski, Interior Minister         50/42           42/43 Stojan Andov, Parliamentary Chairman          48/41           48/39 Branko Crvenkovski, Prime Minister            46/41           44/38 Vlado Popovski, Defense Minister              41/41           36/37 Stevo Crvenkovski, Foreign Minister           40/43   No Data Given Petar Gosev, Democratic Party leader          34/53           40/42 Todor Petrov, Independent parliamentarian     32/53   No Data Given Nikola Popovski, Social Democratic            29/46           32/42    Party parliamentarian    VECER noted that President Gligorov's very high approval rating of 90 percent among those over age 65 fell off to a still high 70 percent among respondents between 18 and 24.  Residents of Skopje ranked the politicians in a slightly different order from the ranking given by the whole sample: Gligorov, Tupurkovski, Frckovski, Andov, Gosev, Branko Crvenkovski, Vlado Popovski, Petrov, Nikola Popovski, and Stevo Crvenkovski.    The results of a series of opinion polls conducted by the Agency for Public Opinion Research and published "exclusively" by the Skopje weekly PULS newspaper, confirmed Gligorov's substantial lead in popularity among political figures.  According to the 31 December 1993 issue of PULS (pages 16-18), the agency gathered the data by means of telephone interviews with 300 residents in the Republic of Macedonia during 20-24 December. PULS also provided data from surveys made in March, June, and September for comparison.  Some of the following percentages are approximate values that were derived from the graph published by the paper:                          March       June      September    December Kiro Gligorov             87          82.33      89.33           89 Stevo Crvenkovski         54          65         49              63 Stojan Andov              61          62         60              61 Branko Crvenkovski        56          60         54 53.5 Ljubomir Frckovski        35          45         48              50 Petar Gosev               50          31         52 49.53 Jovan Andonov,  Deputy Prime Minister    39          39         50              37 Vlado Popovski            18          25         36              35 Kiro Popovski, Deputy  Chairman, Parliament     26          27         33              32 Ante Popovski, leader of  MAAK (Movement for All-  Macedonian Action)       29          32         32 indistinct Jane Miljovski, Minister  without Portfolio        --          23         31              24 Vladimir Golubovski  VMRO-DP (Internal  Macedonian Revolutionary  Organization-Democratic  Party) leader            --          30         25              23 Nevzat Halili  Party for Democratic  Prosperity official      38.33       38         18              18 Lj upco Georgievski VMRO-DPMNE (Internal Macedonian Revolutionary Organization-Democratic Party for Macedonian National Unity) official                  18          10         16              17 Dosta Dimovska VMRO-DPMNE official                  --          11         17              16    On pages 6 and 7 of its 15-16 January issue, VECER also published the results of a November 1993 survey on party preferences. "BriMa," working with the Gallup organization, interviewed 1,036 people.    Question: "If elections were held today, for which party would you vote?" (all numbers are percentages) SDSM (Social Democratic Alliance of Macedonia)  22.8 VMRO-DPMNE                                      11.2 Democratic Party (DP, led by Petar Gosev)        6.3 Socialist Party                                  3.3 Liberal Party (LP)                               3.2 Workers Party                                    2.9 PCERM (Party for the Full Emancipation of     Romanies in Macedonia)                       1.8 Democratic Party of Turks in Macedonia           0.8 MAAK                                             0.3 Another party                                    4.0 Undecided                                       18.6 Would not vote                                   6.6    VECER noted that some parties fared better in certain cities than their overall scores indicate.  For example, the DP was about twice as popular in Skopje as elsewhere, getting 12.1 percent in the capital; the VMRO-DPMNE was more popular in Bitola, getting 15.7 percent, than in the remainder of the country; and the LP in the Bregalnica area got the support of 10.6 percent, substantially higher than the 3.2 percent support it received overall.    Question: "Do you have confidence in the following parties?" (all numbers are percentages)               Yes           No       Do Not Know SDSM           28           51          21 VMRO-DPMNE     15           72          14 LP             19           59          22 PDP-NDP*       20           73           7 *Party for Democratic Prosperity-People's Democratic Party    The poll clearly indicated that Macedonians have little confidence in any of the parties currently active in the country. Respondents were also asked whether it would be good for the country to have elections sooner than scheduled; 62 percent agreed, 20 percent disagreed, and 18 percent did not know. These findings were correlated with party preferences, producing the following results: Of those who would vote for the SDSM, 54 percent wanted elections soon, while 34 percent were against early elections. However, 80 percent of VMRO-DPMNE supporters favored elections soon, as did 79 percent of LP supporters and 71 percent of DP supporters. While 80 percent of those surveyed thought that a person should vote (14 percent did not agree), only 40 percent thought that it was very important which party won the elections and 27 percent thought it was somewhat significant.    (AUTHOR:  GALYEAN.  QUESTIONS AND/OR COMMENTS, PLEASE CALL CHIEF, BALKANS BRANCH AT (703) 733-6481) ELAG/25 February/POLCHF/EED/DEW 28/2023Z FEB </TEXT></DOC>"""
p = Parser(str_doc)
'''

f_counter = None

semaphore = None
m_arr = [Lock(), Lock(), Lock(), Lock(), Lock(), Lock(), Lock()]


def init_sem(sem):
    global semaphore
    semaphore = sem


def do_work(payload):
    with semaphore:
        return payload


def init_counter(args):
    ''' store the counter for later use '''
    global counter
    counter = args


def analyze_data(args):
    ''' increment the global counter, do something with the input '''
    global counter
    # += operation is not atomic, so we need to get a lock:
    with counter.get_lock():
        counter.value += 1
    return args * 10


class ReadFile:
    f_counter = 0
    files_list = []
    complete_list = []
    mutex = Lock()
    controller = None
    percent = 0
    #window = None
    stemmer = None
    indexer = Indexer('C:\\Users\\edoli\\Desktop\\SE_PA')
    semaphore = None
    hash_stopwords = {}
    hash_keywords_months = {}
    hash_keywords_prices = {}
    hash_punc = {}
    hash_punc_middle = {}

    def do_job(id):
        with semaphore:
            sleep(1)
        print("Finished job")

    vocabulary = {}
    hash_terms_collection = {}

    # indexer = Indexer('C:/Users/edoli/Desktop/SE_PA')
    # ('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus'):
    # ('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus\\corpus'):
    # ('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus\\FB396001'):

    def init_globals(self, f_c):
        global f_counter
        f_counter = f_c

    def __init__(self, data_path, stopword_path, stemmer,controller):
        print("***** " + data_path + " *****")
        print("***** " + stopword_path + " *****")
        print('\n' * 100)
        print('Progess:[' + ' ' * 100 + '%0' ']')
        self.controller = controller
        self.stemmer = stemmer

    def set_stopwords(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        list_stopwords = data.split()
        for word in list_stopwords:
            self.hash_stopwords[word] = ""
        del list_stopwords

    def set_keywords_months(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        list_keywords_months = data.split()
        for word in list_keywords_months:
            self.hash_keywords_months[word] = ""
        del list_keywords_months

    def set_keywords_prices(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        list_keywords_prices = data.split()
        for word in list_keywords_prices:
            self.hash_keywords_prices[word] = ""
        del list_keywords_prices

    def set_puncwords(self):
        list_punc = {',', '"', '.', '?', '-', '_', '.', '*', '"', '`', ':', ';', "'", '[', ']', '(', ')', '{', "}", '<',
                     '>', '|', '~',
                     '^', '?', "\"", '\"', '&', '"!"', '!', "=", '+', "#", '\n', "\"", '\"', "/", "\\"}
        for word in list_punc:
            self.hash_punc[word] = ""
        del list_punc

    def set_middlewords(self):
        list_punc = {'|', '.', '..', '...', '>', ';', '^', '?', '\"', '!', "=", '+', "#", "\\"}
        for word in list_punc:
            self.hash_punc_middle[word] = ""
        del list_punc

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
        with open('resources\\cities_data.pkl', 'rb') as input:
            self.hash_cities = pickle.load(input)

    def start_evaluating(self):
        global f_counter
        f_counter = multiprocessing.Value('i', 0)
        start = time.time()
        files_list = self.set_file_list()
        manager = Manager()
        hash_c = manager.dict()
        voc = manager.dict()
        pool = multiprocessing.Pool(processes=8, initializer=self.init_globals, initargs=(f_counter,))
        i = pool.map_async(self.parse_file, files_list, chunksize=1)
        i.wait()
        print(i.get())
        #self.indexer.sort_file_list()
        end = time.time()
        print('total time (s)= ' + str(end - start))
        print(self.complete_list)
        print(*self.complete_list, sep="\n")
        # mutex_arr = Array('i', m_arr)
        # p = Pool(initializer=init_counter, initargs=(counter,))
        # i = p.map_async(analyze_data, self.set_file_list(), chunksize=1)
        # i.wait()

        # sem = multiprocessing.Semaphore(0)
        # with multiprocessing.Pool(processes=4, initializer=(init_counter, init_sem), initargs=(self.f_counter, sem)) as p:
        # results = p.map(do_work, 4)

    def set_file_list(self):
        files_list = []
        for root, dirs, files in os.walk('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus'):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        return files_list

    def parse_file(self, file_path):
        if len(self.hash_stopwords) == 0:
            self.init_helpers()
        global f_counter
        p = None
        file_terms = {}
        p_name = "#NUM_" + str(f_counter.value)
      #  print("process #NUM_" + str(f_counter.value))
        #file_path = args[0]
        #hash_c = args[1]
        #voc = args[2]
        with f_counter.get_lock():
            # print(file_path)
            f_counter.value += 1
            # print(f_counter.value)
        sum = 0
        summary = 0
        f_start = time.time()
        p = Parser(self.hash_stopwords,self.hash_keywords_months,self.hash_keywords_prices,self.hash_punc,self.hash_punc_middle,self.stemmer)
        self.get_doc_from_file(file_path, p)
        #print(p_name +' size :' +str(len(file_terms)))
        #self.merge_file_terms(file_terms)
        #file_terms = {}
        #with f_counter.get_lock():
        #if f_counter.value % 10 == 0:
            #h = hash_c.copy()
            #self.indexer.write_temp_posts(self.hash_terms_collection)
        with open('C:\\Users\\edoli\\Desktop\\SE_PA\\temp_hash_objects\\file_hash_'+ p_name+'.pkl' , 'wb') as output:
            pickle.dump(p.hash_terms, output, pickle.HIGHEST_PROTOCOL)
        #self.indexer.write_temp_posts(p.hash_terms)
       # self.indexer.sort_file_list()
        #     pickle.dump(p.hash_terms, output, pickle.HIGHEST_PROTOCOL)
        file_terms = {}
        self.vocabulary = {}
        f_end = time.time()
        time_to_file = f_end - f_start
        if f_counter.value % 20 == 0:
            p_c = float(f_counter.value)
            p_c = int(p_c * 100 / 1815)
            if p_c != self.percent:
                self.percent = p_c
                self.print_prog(p_c)

    def print_prog(self, p_c):
        print('\n'*100)
        #self.clear()
        print('Progess:[' + '*'*p_c + ' '*(100-p_c) +str(p_c) + '%' ']')



    def get_doc_from_file(self, file_path, parser_object):
        skip_one = 0
        with open(file_path, 'r') as file:
            # data = file.read().replace('\n', '')
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
                    # sem.acquire()
                    parser_object.start_parse(doc)
                    # test_hash = {}
                    # self.indexer.write_temp_posts(test_hash)
                    # self.voc2str(hash_terms)
                    # sem.release()
                    # self.indexer.write_temp_posts(hash_terms)
                    # self.indexer.sort_file_list('C:\\Users\\edoli\\Desktop\\SE_PA\\temp_files\\abc.txt')
                    # self.indexer.write_temp_posts(hash_terms)
                    #self.indexer.sort_file_list('C:\\Users\\edoli\\Desktop\\SE_PA\\temp_files\\abc.txt')

                else:
                    skip_one = 1

        """
        if parser_object.hash_cities.__sizeof__() > 0:
            hash_cities = copy.deepcopy(parser_object.hash_cities)
            obj_api = API(hash_cities)
            obj_api.get_api_info()
        """

        # print(doc_counter2)
        del data_list

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
