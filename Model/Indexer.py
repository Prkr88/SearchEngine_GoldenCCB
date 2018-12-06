import os
import copy
import shutil
import multiprocessing
import pickle
from numpy import log2

LOWERCASE = 0
UPPERCASE = 1
LOWERBOUND = 0
UPPERBOUND = 1


########################################################################################################################
# Class Indexer:                                                                                                       #
#                                                                                                                      #
# Called after ReadFile is finished. Goes over the temporary pickle files (that contain the hash                       #
# dictionaries per each file) and writes them to alphabetical posting files appropriately (explained in the report)    #
# - Runs 2 Process Pools -                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# DECOMPRESSED FORMAT: DAKAR|{'tf_c': 8192, 'df': 1286, 'idf: 22.81, 'hash_docs': {'FBIS3-638': {'tf_d': 1, 'h': 0},   #
#                                               'FBIS3-841': {'tf_d': 1, 'h': 0}, 'FBIS3-880': {'tf_d': 1, 'h': 0},    #
#                                                   'FBIS4-31': {'tf_d': 1, 'h': 0} , 'FBIS4-37': {'tf_d': 1, 'h': 0}}}#
#                                                                                                                      #
# COMPRESSED FORMAT: DAKAR|8192,1286,22.81<FBIS3-638:1,0>203:1.0>39:1,0>FBIS4-31:1,0>6:1,0                             #
########################################################################################################################


class Indexer:

    # constructor #

    def __init__(self, user_path, N_docs):
        self.posting_path = user_path + "/Engine_Data/posting_files"
        self.engine_data_path = user_path + "/Engine_Data"
        self.file_path0 = self.posting_path + '/num.txt'
        self.file_path1 = self.posting_path + '/ab.txt'
        self.file_path2 = self.posting_path + '/cd.txt'
        self.file_path3 = self.posting_path + '/ef.txt'
        self.file_path4 = self.posting_path + '/gh.txt'
        self.file_path5 = self.posting_path + '/ijk.txt'
        self.file_path6 = self.posting_path + '/lmn.txt'
        self.file_path7 = self.posting_path + '/opq.txt'
        self.file_path8 = self.posting_path + '/rs.txt'
        self.file_path9 = self.posting_path + '/tuv.txt'
        self.file_path10 = self.posting_path + '/wxyz.txt'
        self.file_list = [self.file_path0, self.file_path1, self.file_path2, self.file_path3, self.file_path4,
                          self.file_path5,self.file_path6, self.file_path7, self.file_path8, self.file_path9, self.file_path10]
        self.counter = 0
        self.hash_collector = {}
        self.N = N_docs
        self.number_of_files = 0

    # initializes mutexes #

    def init_globals(self, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, f_c):
        global lock0
        global lock1
        global lock2
        global lock3
        global lock4
        global lock5
        global lock6
        global lock7
        global lock8
        global lock9
        global lock10
        global file_counter
        lock0 = l0
        lock1 = l1
        lock2 = l2
        lock3 = l3
        lock4 = l4
        lock5 = l5
        lock6 = l6
        lock7 = l7
        lock8 = l8
        lock9 = l9
        lock10 = l10
        file_counter = f_c

    # main function of the indexing sequence. initializes 2 process pools #

    def start_indexing(self):
        global lock0
        global lock1
        global lock2
        global lock3
        global lock4
        global lock5
        global lock6
        global lock7
        global lock8
        global lock9
        global lock10
        global file_counter
        lock0 = multiprocessing.Value('i',0)
        lock1 = multiprocessing.Value('i',1)
        lock2 = multiprocessing.Value('i',2)
        lock3 = multiprocessing.Value('i',3)
        lock4 = multiprocessing.Value('i',4)
        lock5 = multiprocessing.Value('i',5)
        lock6 = multiprocessing.Value('i',6)
        lock7 = multiprocessing.Value('i',7)
        lock8 = multiprocessing.Value('i',8)
        lock9 = multiprocessing.Value('i',9)
        lock10 = multiprocessing.Value('i',10)
        file_counter = multiprocessing.Value('i',0)
        hash_list = self.set_file_list()
        self.number_of_files = len(hash_list)

        # pool1: loads hash files.pkl to memory, and writes them to 11 temp post.txt files on disk #
        pool1 = multiprocessing.Pool(processes=4, initializer=self.init_globals, initargs=(lock0,lock1,lock2,lock3,lock4,lock5,lock6,lock7,lock8,lock9,lock10 ,file_counter))
        i1 = pool1.map_async(self.write_temp_posts, hash_list, chunksize=1)
        i1.wait()

        # pool2: loads, merges and sorts the posting files #
        file_counter.value = 0
        pool2 = multiprocessing.Pool(processes=4, initializer=self.init_globals, initargs=(lock0,lock1,lock2,lock3,lock4,lock5,lock6,lock7,lock8,lock9,lock10,file_counter))
        i2 = pool2.map_async(self.merger, self.file_list, chunksize=1)
        i2.wait()

        # c = 0
        # for path in hash_list:
        #     if (c==30):
        #         break
        #     else:
        #         self.write_temp_posts_coded(path)
        #         print('done merge #: ' + str(c))
        #         c += 1
        # for m_path in self.file_list:
        #     self.merger(m_path)

    # function sets path list for the process work #

    def set_file_list(self):
        files_list = []
        for root, dirs, files in os.walk(self.engine_data_path + '/temp_hash_objects'):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        return files_list

    # main function writes dictionaries to the temporary posting files #

    def write_temp_posts(self, hash_path):
        global lock0
        global lock1
        global lock2
        global lock3
        global lock4
        global lock5
        global lock6
        global lock7
        global lock8
        global lock9
        global lock10
        global file_counter

        if file_counter.value % 20 == 0:
            p_c = float(file_counter.value)
            p_c = int(p_c * 100 / self.number_of_files)
            self.print_prog(p_c, "Indexing:\n")

        with file_counter.get_lock():
            file_counter.value += 1

        with open(hash_path, 'rb') as input:
            hash_terms = pickle.load(input)

        p0 = self.file_path0
        p1 = self.file_path1
        p2 = self.file_path2
        p3 = self.file_path3
        p4 = self.file_path4
        p5 = self.file_path5
        p6 = self.file_path6
        p7 = self.file_path7
        p8 = self.file_path8
        p9 = self.file_path9
        p10 = self.file_path10

        condition_list = [[[48, 57], [48, 57]], [[65, 66], [97, 98]], [[67, 68], [99, 100]], [[69, 70], [101, 102]], [[71, 72], [103, 104]], [[73, 75], [105, 107]], [[76, 78], [108, 110]], [[79, 81], [111, 113]], [[82, 83], [114, 115]], [[84, 86], [116, 118]], [[87, 90], [119, 122]]]
        posting_list = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
        mutex_list = [lock0, lock1, lock2, lock3, lock4, lock5, lock6, lock7, lock8, lock9, lock10]
        tuple_terms = sorted(hash_terms.items(), key=lambda x: x[0].lower())
        hash_collector = {}
        size = len(posting_list)

        for posting_index in range(0, size):
            collection_index = 0
            with mutex_list[posting_index].get_lock():
                with open(posting_list[posting_index], 'a', encoding='utf-8') as curr_file:
                    for ikey, ival in tuple_terms:
                        resume = True
                        if ikey == "'" or (posting_index == 0 and ikey == '#doc_number'):
                            collection_index += 1
                            resume = False
                        if resume:
                            docs_val = self.load_nested_documents(ival)
                            if docs_val != "CodingException":
                                try:
                                    ch = ikey[0]
                                    if ch == "'" or (posting_index == 0 and ch == '$'):
                                        ikey = ikey[1:]
                                        ch = ikey[0]
                                    if condition_list[posting_index][LOWERCASE][LOWERBOUND] <= ord(ch) <= condition_list[posting_index][LOWERCASE][UPPERBOUND] or condition_list[posting_index][UPPERCASE][LOWERBOUND] <= ord(ch) <= condition_list[posting_index][UPPERCASE][UPPERBOUND]:
                                        try:
                                            curr_file.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                                        except Exception:
                                            hash_collector[str(ikey)] = "WriteToFileException"
                                        collection_index += 1
                                    elif posting_index < (size-1) and (condition_list[posting_index+1][LOWERCASE][LOWERBOUND] <= ord(ch) <= condition_list[size-1][LOWERCASE][UPPERBOUND] or condition_list[posting_index+1][UPPERCASE][LOWERBOUND] <= ord(ch) <= condition_list[size-1][UPPERCASE][UPPERBOUND]):
                                        break
                                    else:
                                        hash_collector[str(ikey)] = "CollectionCharValue"
                                        collection_index += 1
                                except Exception:
                                    hash_collector[str(ikey)] = "WriteToFileException"
                                    collection_index += 1
                    curr_file.close()
            for x in range(0, collection_index):
                del tuple_terms[0]

    # functions compresses the documents list #
    
    def load_nested_documents(self, nest):
        docs_val = ""
        try:
            first_full_id = list(nest['hash_docs'].keys())[0]
            first_list = first_full_id.split('-')
            first_doc_id = first_list[0]
            prev_gap_id = int(first_list[1])
            for j_key, j_val in nest['hash_docs'].items():
                curr_list = j_key.split('-')
                curr_doc_id = curr_list[0]
                curr_gap_id = int(curr_list[1])
                if curr_gap_id != prev_gap_id:  # next doc
                    if curr_doc_id == first_doc_id:  # same doc id
                        temp = curr_gap_id
                        curr_gap_id = curr_gap_id - prev_gap_id
                        if curr_gap_id < 1:
                            curr_gap_id = temp
                            curr_doc_id = curr_doc_id + "-"
                            prev_gap_id = curr_gap_id
                        else:
                            prev_gap_id = temp
                            curr_doc_id = ""
                    else:
                        first_doc_id = curr_doc_id  # new doc id
                        curr_doc_id = curr_doc_id + "-"
                        prev_gap_id = curr_gap_id
                elif curr_doc_id == first_doc_id:  # 1st iteration same doc
                    curr_doc_id = curr_doc_id + "-"
                else:
                    first_doc_id = curr_doc_id  # different doc same gap
                    curr_doc_id = curr_doc_id + "-"
                    prev_gap_id = curr_gap_id
                docs_val = docs_val + str(curr_doc_id) + str(curr_gap_id) + ":" + str(j_val['tf_d']) + "," + str(
                    j_val['h']) + ">"
        except Exception:
            docs_val = "CodingException"
        return docs_val

    # main functions for merging temp posting files to the final posting files. receives path of the temp posting files #

    def merger(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            list_terms = [line.strip() for line in file]
            file.close()
        hash_file_terms = {}
        hash_collector = {}
        for term in list_terms:
            other_tf_c = 0
            other_df = 0
            other_doc_id = ""
            hash_temp_doc = {}
            list_term = term.split('|')
            this_term = None
            other_term = list_term[0]
            if other_term == "island's":
                skip = False
            skip = False
            if other_term != '':
                try:
                    value_term = list_term[1].split('>')
                    get_val = value_term[0].split(',')
                    other_tf_c = int(get_val[0])
                    other_df = int(get_val[1])
                    other_header = int(get_val[3])
                    info_list = get_val[2].split('<')
                    info_list = info_list[1].split(':')
                    other_doc_id = info_list[0]
                    other_tf_d = int(info_list[1])
                    hash_temp_doc.update({other_doc_id: {'tf_d': other_tf_d, 'h': other_header}})
                    prev_doc_id = other_doc_id.split('-')[0]
                    prev_gap_id = int(other_doc_id.split('-')[1])
                    del value_term[0], get_val, info_list
                    while len(value_term) > 1:  # starts from 2nd iteration
                        info_list = value_term[0].split(':')
                        curr_full_doc_id = info_list[0]
                        if curr_full_doc_id[0].isdigit():  # same doc id
                            curr_doc_id = int(curr_full_doc_id)
                            curr_id = curr_doc_id + prev_gap_id
                            other_doc_id = str(prev_doc_id) + "-" + str(curr_id)
                            info_list = info_list[1].split(':')
                            info_list = info_list[0].split(',')
                            other_tf_d = int(info_list[0])
                            other_header = int(info_list[1])
                            hash_temp_doc.update({other_doc_id: {'tf_d': other_tf_d, 'h': other_header}})
                            prev_gap_id = curr_id
                        else:
                            other_doc_id = curr_full_doc_id  # new doc id
                            info_list = info_list[1].split(',')
                            other_tf_d = int(info_list[0])
                            other_header = int(info_list[1])
                            hash_temp_doc.update({other_doc_id: {'tf_d': other_tf_d, 'h': other_header}})
                            last_info = curr_full_doc_id.split('-')
                            prev_doc_id = last_info[0]
                            prev_gap_id = int(last_info[1])
                        del value_term[0]
                    del list_term
                except Exception:
                    hash_collector[str(other_term)] = str(other_doc_id) + "DecodeException"
                    skip = True
                if not skip:
                    this_term = None
                    if self.is_first_upper(other_term):  # other = PEN
                        if other_term in hash_file_terms:  # (1) other=PEN and dict=PEN -> update
                            this_term = hash_file_terms[other_term]
                        else:  # (2) other=PEN and dict=pen -> update
                            temp_term_lower = other_term.lower()  # temp=pen
                            if temp_term_lower in hash_file_terms:  # (2) other=PEN and dict=pen -> update
                                this_term = hash_file_terms[temp_term_lower]
                        if this_term is not None:
                            try:
                                this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                                this_term['hash_docs'].update(hash_temp_doc)
                            except Exception:
                                hash_collector[str(other_term)] = str(other_doc_id) + "MergeTermException"
                            pass  # end of update (1+2)
                        else:  # (5) if its a new term (other=PEN and dict='none')
                            nested_hash = ({'tf_c': other_tf_c, 'df': other_df, 'hash_docs': hash_temp_doc})
                            hash_file_terms[other_term] = nested_hash
                            pass  # end of adding a new term
                    else:  # if the current term is lower case 'pen'
                        if other_term in hash_file_terms:  # (3) other=pen and dict=pen -> update
                            this_term = hash_file_terms[other_term]
                            try:
                                this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                                this_term['hash_docs'].update(hash_temp_doc)
                            except Exception:
                                hash_collector[str(other_term)] = str(other_doc_id) + "MergeTermException"
                            pass  # end of update (3)
                        else:  # (4) other=pen and Dict=PEN  -> now will be Dict=pen + update
                            temp_term_upper = other_term.upper()  # temp = PEN
                            if temp_term_upper in hash_file_terms:
                                old_term_nest = hash_file_terms[temp_term_upper]  # old_term = PEN
                                this_term = copy.deepcopy(old_term_nest)  # creates new lower case term 'pen'
                                try:
                                    this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                                    this_term['hash_docs'].update(hash_temp_doc)
                                except Exception:
                                    hash_collector[str(other_term)] = str(other_doc_id) + "MergeTermException"
                                hash_file_terms[other_term] = this_term  # adds 'pen'
                                del hash_file_terms[temp_term_upper]  # deletes old upper case term 'PEN'
                                pass  # end of update (4)
                            else:  # (5) if its a new term (other=pen and dict='none')
                                nested_hash = ({'tf_c': other_tf_c, 'df': other_df, 'hash_docs': hash_temp_doc})
                                hash_file_terms[other_term] = nested_hash
                                pass
        hash_check = self.hash_filter(path)
        with open(path, 'w', encoding='utf-8') as file:
            file.close()
        with open(path, 'a', encoding='utf-8') as file:
            hash_file_terms = sorted(hash_file_terms.items(), key=lambda x: x[0].lower())
            for ikey, ival in hash_file_terms:
                try:
                    docs_val = self.load_nested_documents(ival)
                    if docs_val != "CodingException":
                        ch = ikey[0]
                        if hash_check is not None:
                            if ch in hash_check:
                                try:
                                    file.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                                        float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                                except Exception:
                                    hash_collector[str(ikey)] = "WriteFileException"
                        else:
                            hash_collector[str(ikey)] = "HashCheckException"
                    else:
                        hash_collector[str(ikey)] = "CodingException"
                except Exception:
                    a = 0
            file.close()
        hash_file_terms = {}
        with file_counter.get_lock():
            file_counter.value += 1
            p_c = float(file_counter.value)
            p_c = int(p_c * 100 / 11)
            self.print_prog(p_c, "Sorting Index:\n")

    def collector_filter(self, path, hash_collector):
        junk_path = path + "-junk.txt"
        with open(junk_path, 'a', encoding='utf-8') as file:
            hash_collector = sorted(hash_collector.items(), key=lambda x: x[0].lower())
            for ikey, ival in hash_collector:
                file.write(str(ikey) + '\n')
            file.close()
        hash_collector = []

    def hash_filter(self, path):
        hash_check = {}
        if "num.txt" in path:
            hash_check = {'0': "", '1': "", '2': "", '3': "", '4': "", '5': "", '6': "", '7': "", '8': "", '9': ""}
        elif "ab.txt" in path:
            hash_check = {'a': "", 'A': "", 'b': "", 'B': ""}
        elif "cd.txt" in path:
            hash_check = {'c': "", 'C': "", 'd': "", 'D': ""}
        elif "ef.txt" in path:
            hash_check = {'e': "", 'E': "", 'f': "", 'F': ""}
        elif "gh.txt" in path:
            hash_check = {'g': "", 'G': "", 'h': "", 'H': ""}
        elif "ijk.txt" in path:
            hash_check = {'i': "", 'I': "", 'j': "", 'J': "", 'k': "", 'K': ""}
        elif "lmn.txt" in path:
            hash_check = {'l': "", 'L': "", 'm': "", 'M': "", 'n': "", 'N': ""}
        elif "opq.txt" in path:
            hash_check = {'o': "", 'O': "", 'p': "", 'P': "", 'q': "", 'Q': ""}
        elif "rs.txt" in path:
            hash_check = {'r': "", 'R': "", 's': "", 'S': ""}
        elif "tuv.txt" in path:
            hash_check = {'t': "", 'T': "", 'u': "", 'U': "", 'v': "", 'V': ""}
        elif "wxyz.txt" in path:
            hash_check = {'w': "", 'W': "", 'x': "", 'X': "", 'y': "", 'Y': "", 'z': "", 'Z': ""}
        return hash_check

    def is_first_upper(self, term):  # NOTE: to check terms like fRog or just Frog?
        try:
            return 64 < ord(term[0]) < 91
        except IndexError:
            pass

    def is_fully_upper(self, term):
        if len(term) > 1:
            return 64 < ord(term[0]) < 91 and 64 < ord(term[1]) < 91
        else:
            return 64 < ord(term[0]) < 91

    def reset_posting_files(self):
        if self.posting_path is not None:
            if os.path.exists(self.engine_data_path):
                shutil.rmtree(self.engine_data_path)

    def print_prog(self, p_c ,op):
        print('\n'*100)
        print(op + '[' + '*'*int(p_c/2) + ' '*int((100-p_c)/2) +str(p_c) + '%' ']')
