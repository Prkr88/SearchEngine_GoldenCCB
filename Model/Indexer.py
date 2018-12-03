import os
import copy
import shutil
import multiprocessing
import pickle
from numpy import log2


########################################################################################################################
# DECODED FORMAT: DAKAR|{'tf_c': 8192, 'df': 1286, 'idf: 22.81, 'hash_docs': {'FBIS3-638': {'tf_d': 1, 'h': 0},        #
#                                               'FBIS3-841': {'tf_d': 1, 'h': 0}, 'FBIS3-880': {'tf_d': 1, 'h': 0},    #
#                                                   'FBIS4-31': {'tf_d': 1, 'h': 0} , 'FBIS4-37': {'tf_d': 1, 'h': 0}}}#
#                                                                                                                      #
# CODED FORMAT: DAKAR|8192,1286,22.81<FBIS3-638:1,0>203:1.0>39:1,0>FBIS4-31:1,0>6:1,0                                  #
########################################################################################################################


class Indexer:

    def __init__(self, user_path):
        self.posting_path = user_path + "/Engine_Data/posting_files"
        if not os.path.exists(self.posting_path):
            os.makedirs(self.posting_path)
        self.file_path0 = self.posting_path + 'num.txt'
        self.file_path1 = self.posting_path + 'ab.txt'
        self.file_path2 = self.posting_path + 'cd.txt'
        self.file_path3 = self.posting_path + 'ef.txt'
        self.file_path4 = self.posting_path + 'gh.txt'
        self.file_path5 = self.posting_path + 'ijk.txt'
        self.file_path6 = self.posting_path + 'lmn.txt'
        self.file_path7 = self.posting_path + 'opq.txt'
        self.file_path8 = self.posting_path + 'rs.txt'
        self.file_path9 = self.posting_path + 'tuv.txt'
        self.file_path10 = self.posting_path + 'wxyz.txt'
        self.file_list = [self.file_path10, self.file_path9, self.file_path8, self.file_path7, self.file_path6,
                          self.file_path5,self.file_path4, self.file_path3, self.file_path2, self.file_path1, self.file_path0]
        self.counter = 0
        self.hash_junk = {}
        self.N = 468000

    def init_globals(self, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10):
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
        hash_list = self.set_file_list()

        ### pool1: loads hash files.pkl to memory, and writes them to 11 temp post.txt files on disk ###
        pool1 = multiprocessing.Pool(processes=4, initializer=self.init_globals, initargs=(lock0,lock1,lock2,lock3,lock4,lock5,lock6,lock7,lock8,lock9,lock10))
        i1 = pool1.map_async(self.write_temp_posts, hash_list, chunksize=1)
        i1.wait()

        ### pool2: loads, merges and sorts the posting files ###
        pool2 = multiprocessing.Pool(processes=4, initializer=self.init_globals, initargs=(lock0,lock1,lock2,lock3,lock4,lock5,lock6,lock7,lock8,lock9,lock10))
        i2 = pool2.map_async(self.merger, self.file_list, chunksize=1)
        i2.wait()

    def set_file_list(self):
        files_list = []
        for root, dirs, files in os.walk(self.posting_path + '\\Engine_Data\\temp_hash_objects'):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        return files_list

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
        with open(hash_path,'rb') as input:
            hash_terms = pickle.load(input)
        hash_terms = sorted(hash_terms.items(), key=lambda x: x[0].lower())
        with lock0.get_lock():
            with open(self.file_path0, 'a', encoding='utf-8') as num:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ikey[0]
                    if ch.isdigit() or ch == '$':
                        num.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 97 <= ord(ch) <= 98 or 65 <= ord(ch) <= 66:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                num.close()
        with lock1.get_lock():
            with open(self.file_path1, 'a', encoding='utf-8') as ab:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 97 <= ch <= 98 or 65 <= ch <= 66:
                        ab.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 99 <= ch <= 100 or 67 <= ch <= 68:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                ab.close()
        with lock2.get_lock():
            with open(self.file_path2, 'a', encoding='utf-8') as cd:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 99 <= ch <= 100 or 67 <= ch <= 68:
                        cd.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 101 <= ch <= 102 or 69 <= ch <= 70:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                cd.close()
        with lock3.get_lock():
            with open(self.file_path3, 'a', encoding='utf-8') as ef:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 101 <= ch <= 102 or 69 <= ch <= 70:
                        ef.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 103 <= ch <= 104 or 71 <= ch <= 72:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                ef.close()
        with lock4.get_lock():
            with open(self.file_path4, 'a', encoding='utf-8') as gh:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 103 <= ch <= 104 or 71 <= ch <= 72:
                        gh.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 105 <= ch <= 107 or 73 <= ch <= 75:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                gh.close()
        with lock5.get_lock():
            with open(self.file_path5, 'a', encoding='utf-8') as ijk:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 105 <= ch <= 107 or 73 <= ch <= 75:
                        ijk.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 108 <= ch <= 110 or 76 <= ch <= 78:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                ijk.close()
        with lock6.get_lock():
            with open(self.file_path6, 'a', encoding='utf-8') as lmn:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 108 <= ch <= 110 or 76 <= ch <= 78:
                        lmn.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 111 <= ch <= 113 or 79 <= ch <= 81:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                lmn.close()
        with lock7.get_lock():
            with open(self.file_path7, 'a', encoding='utf-8') as opq:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 111 <= ch <= 113 or 79 <= ch <= 81:
                        opq.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 114 <= ch <= 115 or 82 <= ch <= 83:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                opq.close()
        with lock8.get_lock():
            with open(self.file_path8, 'a', encoding='utf-8') as rs:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 114 <= ch <= 115 or 82 <= ch <= 83:
                        rs.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 116 <= ch <= 118 or 84 <= ch <= 86:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                rs.close()
        with lock9.get_lock():
            with open(self.file_path9, 'a', encoding='utf-8') as tuv:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 116 <= ch <= 118 or 84 <= ch <= 86:
                        tuv.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    elif 119 <= ch <= 122 or 87 <= ch <= 90:
                        break
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                for x in range(0, i):
                    del hash_terms[0]
                tuv.close()
        with lock10.get_lock():
            with open(self.file_path10, 'a', encoding='utf-8') as wxyz:
                i = 0
                for ikey, ival in hash_terms:
                    try:
                        docs_val = ""
                        first_full_id = list(ival['hash_docs'].keys())[0]
                        first_list = first_full_id.split('-')
                        first_doc_id = first_list[0]
                        last_gap = int(first_list[1])
                        for jkey, jval in ival['hash_docs'].items():
                            curr_list = jkey.split('-')
                            curr_doc_id = curr_list[0]
                            curr_gap = int(curr_list[1])
                            if curr_gap != last_gap:
                                if curr_doc_id == first_doc_id:
                                    temp = curr_gap
                                    curr_gap = curr_gap - last_gap
                                    last_gap = temp
                                    curr_doc_id = ""
                                else:
                                    first_doc_id = curr_doc_id
                                    curr_doc_id = curr_doc_id + "-"
                                    last_gap = curr_gap
                            else:
                                curr_doc_id = curr_doc_id + "-"
                            docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                                jval['h']) + ">"
                    except (ValueError, IndexError):
                        i += 1
                    ch = ord(ikey[0])
                    if 119 <= ch <= 122 or 87 <= ch <= 90:
                        wxyz.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                            float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                        i += 1
                    else:
                        self.hash_junk[ikey] = ""
                        i += 1
                        pass
                wxyz.close()
        hash_terms = {}

    def merger(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            list_terms = [line.strip() for line in file]
            file.close()
        hash_file_terms = {}
        for term in list_terms:
            list_term = term.split('|')
            this_term = None
            other_term = list_term[0]
            skip = False
            if other_term != '':
                try:
                    hash_temp_doc = {}
                    value_term = list_term[1].split('>')
                    get_val = value_term[0].split(',')
                    other_tf_c = int(get_val[0])
                    other_df = int(get_val[1])
                    other_header = int(get_val[3])
                    get_info = get_val[2].split('<')
                    get_info = get_info[1].split(':')
                    other_doc_id = get_info[0]
                    other_tf_d = int(get_info[1])
                    hash_temp_doc.update({other_doc_id: {'tf_d': other_tf_d, 'h': other_header}})
                    last_doc_id = other_doc_id.split('-')[0]
                    last_gap = int(other_doc_id.split('-')[1])
                    del value_term[0], get_val, get_info
                    while len(value_term) > 1:
                        get_info = value_term[0].split(':')
                        curr_full_doc_id = get_info[0]
                        if curr_full_doc_id[0].isdigit():
                            curr_doc_id = int(curr_full_doc_id)
                            curr_id = curr_doc_id + last_gap
                            other_doc_id = str(last_doc_id) + "-" + str(curr_id)
                            get_info = get_info[1].split(':')
                            get_info = get_info[0].split(',')
                            other_tf_d = int(get_info[0])
                            other_header = int(get_info[1])
                            hash_temp_doc.update({other_doc_id: {'tf_d': other_tf_d, 'h': other_header}})
                            last_gap = curr_id
                        else:
                            other_doc_id = curr_full_doc_id
                            get_info = get_info[1].split(',')
                            other_tf_d = int(get_info[0])
                            other_header = int(get_info[1])
                            hash_temp_doc.update({other_doc_id: {'tf_d': other_tf_d, 'h': other_header}})
                            last_info = curr_full_doc_id.split('-')
                            last_doc_id = last_info[0]
                            last_gap = int(last_info[1])
                        del value_term[0]
                    del list_term
                except (ValueError, IndexError):
                    self.hash_junk[other_term] = "DickTermException"
                    skip = True
                if not skip:
                    if self.is_first_upper(other_term):  # other = PEN
                        if other_term in hash_file_terms:  # (1) other=PEN and dict=PEN -> update
                            this_term = hash_file_terms[other_term]
                        else:  # (2) other=PEN and dict=pen -> update
                            temp_term_lower = other_term.lower()  # temp=pen
                            if temp_term_lower in hash_file_terms:  # (2) other=PEN and dict=pen -> update
                                this_term = hash_file_terms[temp_term_lower]
                        if this_term is not None:
                            try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                                this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                                this_term['hash_docs'].update(hash_temp_doc)
                            except KeyError:
                                i = 0
                            pass  # end of update (1+2)
                        else:  # (5) if its a new term (other=PEN and dict='none')
                            nested_hash = ({'tf_c': other_tf_c, 'df': other_df, 'hash_docs': hash_temp_doc})
                            hash_file_terms[other_term] = nested_hash
                            pass  # end of adding a new term
                    else:  # if the current term is lower case 'pen' (if it's an upper case we don't mind)
                        if other_term in hash_file_terms:  # (3) other=pen and dict=pen -> update
                            this_term = hash_file_terms[other_term]
                            try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                                this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                                this_term['hash_docs'].update(hash_temp_doc)
                            except KeyError:
                                i = 0
                            pass  # end of update (3)
                        else:  # (4) other=pen and Dict=PEN  -> now will be Dict=pen + update
                            temp_term_upper = other_term.upper()  # temp = PEN
                            if temp_term_upper in hash_file_terms:
                                old_term = hash_file_terms[temp_term_upper]  # this_term = PEN
                                this_term = copy.deepcopy(old_term)  # creates new lower case term 'pen'
                                try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                                    this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                                    this_term['hash_docs'].update(hash_temp_doc)
                                except KeyError:
                                    i = 0
                                hash_file_terms[other_term] = this_term  # adds 'pen'
                                del hash_file_terms[temp_term_upper]  # deletes old upper case term 'PEN'
                                pass  # end of update (4)
                            else:  # (5) if its a new term (other=pen and dict='none')
                                nested_hash = ({'tf_c': other_tf_c, 'df': other_df, 'hash_docs': hash_temp_doc})
                                hash_file_terms[other_term] = nested_hash
                                pass
        with open(path, 'w', encoding='utf-8') as file:
            file.close()
        with open(path, 'a', encoding='utf-8') as file:
            i = 0
            hash_file_terms = sorted(hash_file_terms.items(), key=lambda x: x[0].lower())
            for ikey, ival in hash_file_terms:
                skip = False
                try:
                    docs_val = ""
                    first_full_id = list(ival['hash_docs'].keys())[0]
                    first_list = first_full_id.split('-')
                    first_doc_id = first_list[0]
                    last_gap = int(first_list[1])
                    for jkey, jval in ival['hash_docs'].items():
                        curr_list = jkey.split('-')
                        curr_doc_id = curr_list[0]
                        curr_gap = int(curr_list[1])
                        if curr_gap != last_gap:
                            if curr_doc_id == first_doc_id:
                                temp = curr_gap
                                curr_gap = curr_gap - last_gap
                                last_gap = temp
                                curr_doc_id = ""
                            else:
                                first_doc_id = curr_doc_id
                                curr_doc_id = curr_doc_id + "-"
                                last_gap = curr_gap
                        else:
                            curr_doc_id = curr_doc_id + "-"
                        docs_val = docs_val + str(curr_doc_id) + str(curr_gap) + ":" + str(jval['tf_d']) + "," + str(
                            jval['h']) + ">"
                except (ValueError, IndexError):
                    self.hash_junk[ikey] = ""
                    skip = True
                if not skip:
                    file.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                    float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
            file.close()
        hash_file_terms = {}

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
            if os.path.exists(self.posting_path):
                shutil.rmtree(self.posting_path)
