import multiprocessing
import os
from asyncio import sleep
from Model.Parser import Parser
from Model.Indexer import Indexer
import time
import gc
import cProfile, pstats
import time
import json
import timeit
from io import StringIO
from multiprocessing import Pool, Lock, Array
from Model.API import API

# ('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus'):
# ('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus\\corpus'):
# ('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus\\FB396001'):
'''
# <F P=104>  Rotterdam NRC HANDELSBLAD </F>
str_doc = """ <DOC><DOCNO> FBIS3-1 </DOCNO><HT>  "cr00000011094001" </HT><HEADER><H2> <F P=104>  Beijing GUANGMING RIBAO </F>   March Reports </H2><DATE1>  1 March 1994 </DATE1>Article Type:FBIS Document Type:FOREIGN MEDIA NOTE--FB PN 94-028 <H3> <TI>      FORMER YUGOSLAV REPUBLIC OF MACEDONIA: OPINION POLLS ON </TI></H3></HEADER><TEXT>matan@gmail.com U.S. edo@gmail.com Summary:  Newspapers in the Former Yugoslav Republic of    Macedonia have published the results of opinion polls,    indicating the relative popularity of politicians,    political parties, and attitudes toward the political system.    The 22-23 January edition of the Skopje newspaper VECER in Macedonian published on pages 6-7 the results of an opinion poll conducted by the "BriMa" agency in November 1993. According to VECER, 1,036 respondents were classified by age and residence, but the paper did not explain the methodology or give the margin of error.  For the purpose of comparison, the paper cited the results of an unidentified poll made in May 1993. The approval/disapproval ratings, in percent, for ten Macedonian politicians were:                                            November 1993    May 1993 Kiro Gligorov, President of the Republic      76/15           78/13 Vasil Tupurkovski, former Macedonian          50/36           43/37    official in Federal Yugoslavia Ljubomir Frckovski, Interior Minister         50/42           42/43 Stojan Andov, Parliamentary Chairman          48/41           48/39 Branko Crvenkovski, Prime Minister            46/41           44/38 Vlado Popovski, Defense Minister              41/41           36/37 Stevo Crvenkovski, Foreign Minister           40/43   No Data Given Petar Gosev, Democratic Party leader          34/53           40/42 Todor Petrov, Independent parliamentarian     32/53   No Data Given Nikola Popovski, Social Democratic            29/46           32/42    Party parliamentarian    VECER noted that President Gligorov's very high approval rating of 90 percent among those over age 65 fell off to a still high 70 percent among respondents between 18 and 24.  Residents of Skopje ranked the politicians in a slightly different order from the ranking given by the whole sample: Gligorov, Tupurkovski, Frckovski, Andov, Gosev, Branko Crvenkovski, Vlado Popovski, Petrov, Nikola Popovski, and Stevo Crvenkovski.    The results of a series of opinion polls conducted by the Agency for Public Opinion Research and published "exclusively" by the Skopje weekly PULS newspaper, confirmed Gligorov's substantial lead in popularity among political figures.  According to the 31 December 1993 issue of PULS (pages 16-18), the agency gathered the data by means of telephone interviews with 300 residents in the Republic of Macedonia during 20-24 December. PULS also provided data from surveys made in March, June, and September for comparison.  Some of the following percentages are approximate values that were derived from the graph published by the paper:                          March       June      September    December Kiro Gligorov             87          82.33      89.33           89 Stevo Crvenkovski         54          65         49              63 Stojan Andov              61          62         60              61 Branko Crvenkovski        56          60         54 53.5 Ljubomir Frckovski        35          45         48              50 Petar Gosev               50          31         52 49.53 Jovan Andonov,  Deputy Prime Minister    39          39         50              37 Vlado Popovski            18          25         36              35 Kiro Popovski, Deputy  Chairman, Parliament     26          27         33              32 Ante Popovski, leader of  MAAK (Movement for All-  Macedonian Action)       29          32         32 indistinct Jane Miljovski, Minister  without Portfolio        --          23         31              24 Vladimir Golubovski  VMRO-DP (Internal  Macedonian Revolutionary  Organization-Democratic  Party) leader            --          30         25              23 Nevzat Halili  Party for Democratic  Prosperity official      38.33       38         18              18 Lj upco Georgievski VMRO-DPMNE (Internal Macedonian Revolutionary Organization-Democratic Party for Macedonian National Unity) official                  18          10         16              17 Dosta Dimovska VMRO-DPMNE official                  --          11         17              16    On pages 6 and 7 of its 15-16 January issue, VECER also published the results of a November 1993 survey on party preferences. "BriMa," working with the Gallup organization, interviewed 1,036 people.    Question: "If elections were held today, for which party would you vote?" (all numbers are percentages) SDSM (Social Democratic Alliance of Macedonia)  22.8 VMRO-DPMNE                                      11.2 Democratic Party (DP, led by Petar Gosev)        6.3 Socialist Party                                  3.3 Liberal Party (LP)                               3.2 Workers Party                                    2.9 PCERM (Party for the Full Emancipation of     Romanies in Macedonia)                       1.8 Democratic Party of Turks in Macedonia           0.8 MAAK                                             0.3 Another party                                    4.0 Undecided                                       18.6 Would not vote                                   6.6    VECER noted that some parties fared better in certain cities than their overall scores indicate.  For example, the DP was about twice as popular in Skopje as elsewhere, getting 12.1 percent in the capital; the VMRO-DPMNE was more popular in Bitola, getting 15.7 percent, than in the remainder of the country; and the LP in the Bregalnica area got the support of 10.6 percent, substantially higher than the 3.2 percent support it received overall.    Question: "Do you have confidence in the following parties?" (all numbers are percentages)               Yes           No       Do Not Know SDSM           28           51          21 VMRO-DPMNE     15           72          14 LP             19           59          22 PDP-NDP*       20           73           7 *Party for Democratic Prosperity-People's Democratic Party    The poll clearly indicated that Macedonians have little confidence in any of the parties currently active in the country. Respondents were also asked whether it would be good for the country to have elections sooner than scheduled; 62 percent agreed, 20 percent disagreed, and 18 percent did not know. These findings were correlated with party preferences, producing the following results: Of those who would vote for the SDSM, 54 percent wanted elections soon, while 34 percent were against early elections. However, 80 percent of VMRO-DPMNE supporters favored elections soon, as did 79 percent of LP supporters and 71 percent of DP supporters. While 80 percent of those surveyed thought that a person should vote (14 percent did not agree), only 40 percent thought that it was very important which party won the elections and 27 percent thought it was somewhat significant.    (AUTHOR:  GALYEAN.  QUESTIONS AND/OR COMMENTS, PLEASE CALL CHIEF, BALKANS BRANCH AT (703) 733-6481) ELAG/25 February/POLCHF/EED/DEW 28/2023Z FEB </TEXT></DOC>"""
p = Parser(str_doc)
'''


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
    indexer = Indexer('C:/Users/edoli/Desktop/SE_PA')
    semaphore = None

    def do_job(id):
        with semaphore:
            sleep(1)
        print("Finished job")



    def __init__(self , data_path,stopword_path):
        self.set_file_list()
        print("***** " +data_path+ " *****")
        print("***** " +stopword_path+ " *****")
        start = time.time()

        # mutex_arr = Array('i', m_arr)
        # p = Pool(initializer=init_counter, initargs=(counter,))
        # i = p.map_async(analyze_data, self.set_file_list(), chunksize=1)
        # i.wait()

        # sem = multiprocessing.Semaphore(0)
        # with multiprocessing.Pool(processes=4, initializer=(init_counter, init_sem), initargs=(self.f_counter, sem)) as p:
            # results = p.map(do_work, 4)

        first_file = self.files_list[0]
        self.get_files(first_file)
        print("Complete")
        end = time.time()
        print('total time (s)= ' + str(end - start))
        print(self.complete_list)
        print(*self.complete_list, sep="\n")

    def set_file_list(self):
        for root, dirs, files in os.walk('C:\\Users\\edoli\\Desktop\\SE_PA\\corpus\\corpus'):
            for file in files:
                file_path = os.path.join(root, file)
                self.files_list.append(file_path)

    def get_files(self, file_path):
        print(file_path)
        self.complete_list.append(file_path)
        vocabulary = {}
        posting = {}
        counter = 0
        sum = 0
        summary = 0
        f_start = time.time()
        p = Parser()
        self.get_doc_from_file(file_path, p)
        counter = counter + 1
        # vocabulary = {**vocabulary, **p.hash_terms}
        # with open(
        #         'C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\hashTermsCheck'
        #         '\\fileNum.' + str(counter)+'.txt','w') as vocb_file:
        #     vocb_file.write(json.dumps(vocabulary, indent=4, separators=(',', ': ')))
        #del p
        #gc.collect()
        f_end = time.time()
        sum += f_end - f_start
        summary = summary + (f_end - f_start)
        #print("time for file #" + str(self.f_counter) + " :" + str(f_end - f_start))
        self.f_counter += 1
        #print("avarage per file: " + str(summary/300))
        #print(counter)

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
                # if doc_counter == 10:
                #     doc_counter = 0
                #     del parser_object
                #     gc.collect()
                #     print("memoey cleared after " + str(doc_counter2) + " documents ")
                #     parser_object = Parser()
                if skip_one == 1:
                    doc_counter += 1
                    doc = "<DOC>" + doc
                    # sem.acquire()
                    hash_terms = parser_object.start_parse(doc)
                    # self.voc2str(hash_terms)
                    # sem.release()
                    self.indexer.write_temp_posts(hash_terms)
                    # self.indexer.sort_file_list('C:\\Users\\edoli\\Desktop\\SE_PA\\temp_files\\abc.txt')

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
        #gc.collect()
        # pr = cProfile.Profile()
        # pr.enable()  # start profiling
        #
        # get_files()
        # pr.disable()  # end profiling
        # s = StringIO()
        # sortby = 'cumulative'
        # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        # ps.print_stats()
        # print(s.getvalue())
        # end = time.time()
        # print("corpus time: " + str(end - start))

    def voc2str(self, hash_voc):
        str_display = ""
        for key in hash_voc:
            str_display = str_display + str(key) + " \n"
        print(str_display)