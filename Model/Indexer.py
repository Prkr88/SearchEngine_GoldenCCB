import os
import copy
import shutil
from multiprocessing import Pool, Lock
from numpy import log2

m_arr = [Lock(), Lock(), Lock(), Lock(), Lock(), Lock(), Lock()]


# FORMAT:  DAKAR|{'tf_c': 8192, 'df': 8192, 'hash_docs': {'FBIS3-638': {'tf_d': 1, 'h': 0}, 'FBIS3-841': {'tf_d': 1, 'h': 0}, 'FBIS3-880': {'tf_d': 1, 'h': 0}, 'FBIS3-884': {'tf_d': 1, 'h': 0}}}
# FORMAT:  DAKAR|


class Indexer:

    def __init__(self, user_path):
        self.posting_path = user_path + "/temp_files/"
        if not os.path.exists(self.posting_path):
            os.makedirs(self.posting_path)
        self.file_path0 = self.posting_path + 'num.txt'
        self.file_path1 = self.posting_path + 'abc.txt'
        self.file_path2 = self.posting_path + 'defgh.txt'
        self.file_path3 = self.posting_path + 'ijklm.txt'
        self.file_path4 = self.posting_path + 'nopqr.txt'
        self.file_path5 = self.posting_path + 'stuvxwyz.txt'
        self.file_list = [self.file_path0, self.file_path1, self.file_path2, self.file_path3, self.file_path4,
                          self.file_path5]
        self.hash_file_terms = {}
        self.counter = 0
        self.hash_junk = {}
        self.N = 468000

        '''
                hash_terms = {'100': {'tf_c': 8192, 'df': 8192, 'hash_docs': {'FBIS3-638': {'tf_d': 1, 'h': 0},  'FBIS3-841': {'tf_d': 1, 'h': 0},
                                'FBIS4-100': {'tf_d': 1, 'h': 0},'FBIS4-105': {'tf_d': 1, 'h': 0}, 'FBIS4-107': {'tf_d': 1, 'h': 0}}},
                      '200': {'tf_c': 8192, 'df': 8192, 'hash_docs': {'FBIS3-638': {'tf_d': 1, 'h': 0},
                                                                       'FBIS3-841': {'tf_d': 1, 'h': 0},
                                                                       'FBIS4-200': {'tf_d': 1, 'h': 0},
                                                                       'FBIS4-202': {'tf_d': 1, 'h': 0}}}}
                                                                       '''

    def write_temp_posts(self, hash_terms):
        hash_terms = sorted(hash_terms.items(), key=lambda x: x[0].lower())
        m_arr[0].acquire()
        with open(self.file_path0, 'a', encoding='utf-8') as num:
            i = 0
            for ikey, ival in hash_terms:
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
                ch = ikey[0]
                if ch.isdigit() or ch == '$':
                    num.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                        float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                    i += 1
                elif 97 <= ord(ch) <= 99 or 65 <= ord(ch) <= 67:
                    break
                else:
                    self.hash_junk[ikey] = ""
                    i += 1
                    pass
            for x in range(0, i):
                del hash_terms[0]
            num.close()
        m_arr[0].release()
        m_arr[1].acquire()
        with open(self.file_path1, 'a', encoding='utf-8') as abc:
            i = 0
            for ikey, ival in hash_terms:
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
                ch = ord(ikey[0])
                if 97 <= ch <= 99 or 65 <= ch <= 67:
                    abc.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                        float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                    i += 1
                elif 100 <= ch <= 104 or 68 <= ch <= 72:
                    break
                else:
                    self.hash_junk[ikey] = ""
                    i += 1
                    pass
            for x in range(0, i):
                del hash_terms[0]
            abc.close()
        m_arr[1].release()
        m_arr[2].acquire()
        with open(self.file_path2, 'a', encoding='utf-8') as defgh:
            i = 0
            for ikey, ival in hash_terms:
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
                ch = ord(ikey[0])
                if 100 <= ch <= 104 or 68 <= ch <= 72:
                    defgh.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                        float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                    i += 1
                elif 105 <= ch <= 109 or 73 <= ch <= 77:
                    break
                else:
                    self.hash_junk[ikey] = ""
                    i += 1
                    pass
            for x in range(0, i):
                del hash_terms[0]
            defgh.close()
        m_arr[2].release()
        m_arr[3].acquire()
        with open(self.file_path3, 'a', encoding='utf-8') as ijklm:
            i = 0
            for ikey, ival in hash_terms:
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
                ch = ord(ikey[0])
                if 105 <= ch <= 109 or 73 <= ch <= 77:
                    ijklm.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                        float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                    i += 1
                elif 110 <= ch <= 114 or 78 <= ch <= 82:
                    break
                else:
                    self.hash_junk[ikey] = ""
                    i += 1
                    pass
            for x in range(0, i):
                del hash_terms[0]
            ijklm.close()
        m_arr[3].release()
        m_arr[4].acquire()
        with open(self.file_path4, 'a', encoding='utf-8') as nopqr:
            i = 0
            for ikey, ival in hash_terms:
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
                ch = ord(ikey[0])
                if 110 <= ch <= 114 or 78 <= ch <= 82:
                    nopqr.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                        log2(self.N / ival['df'])) + "<" + str(docs_val) + '\n')
                    i += 1
                elif 115 <= ch <= 122 or 83 <= ch <= 90:
                    break
                else:
                    self.hash_junk[ikey] = ""
                    i += 1
                    pass
            for x in range(0, i):
                del hash_terms[0]
            nopqr.close()
        m_arr[4].release()
        m_arr[5].acquire()
        with open(self.file_path5, 'a', encoding='utf-8') as stuvxwyz:
            i = 0
            for ikey, ival in hash_terms:
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
                ch = ord(ikey[0])
                if 115 <= ch <= 122 or 83 <= ch <= 90:
                    stuvxwyz.write(str(ikey) + "|" + str(ival['tf_c']) + "," + str(ival['df']) + "," + str(
                        float("{0:.2f}".format(log2(self.N / ival['df'])))) + "<" + str(docs_val) + '\n')
                    i += 1
                else:
                    self.hash_junk[ikey] = ""
                    i += 1
                    pass
            stuvxwyz.close()
        m_arr[5].release()
        hash_terms = {}

        # self.counter += 1
        # if self.counter == 5:
        #     self.sort_file_list(self.file_path1)
        # self.sort_file_hash(self.file_path1)
        # self.sort_file_list(self.file_path1)

    '''
    def sort_file_hash(self):
        list_files = []
        hash_terms = {}
        with open(file, 'a', encoding='utf-8') as file:
            for line in file:
                (key, val) = line.split()
                self.hash_file_terms[int(key)] = val
            file.close()
        for term in hash_terms:
            self.merger(term)
        self.write_temp_posts(self.hash_file_terms)
    '''

    def sort_file_list(self):
        file_list = self.file_list
        for file in file_list:
            with open(file, 'r', encoding='utf-8') as file:
                list_terms = [line.strip() for line in file]
                file.close()
            for term in list_terms:
                term = term.split('|')
                self.merger(term)  # merges to self.hash_file_terms
            with open(file, 'w', encoding='utf-8') as file:
                file.close()
            self.write_temp_posts(self.hash_file_terms)

    # FORMAT:  DAKAR|{'tf_c': 8192, 'df': 8192, 'hash_docs': {'FBIS3-638': {'tf_d': 1, 'h': 0}, 'FBIS3-841': {'tf_d': 1, 'h': 0}, 'FBIS3-880': {'tf_d': 1, 'h': 0}, 'FBIS3-884': {'tf_d': 1, 'h': 0}}}

    def merger(self, list_term):
        this_term = None
        other_term = list_term[0]
        if other_term != '':
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
            if self.is_first_upper(other_term):  # other = PEN
                if other_term in self.hash_file_terms:  # (1) other=PEN and dict=PEN -> update
                    this_term = self.hash_file_terms[other_term]
                else:  # (2) other=PEN and dict=pen -> update
                    temp_term_lower = other_term.lower()  # temp=pen
                    if temp_term_lower in self.hash_file_terms:  # (2) other=PEN and dict=pen -> update
                        this_term = self.hash_file_terms[temp_term_lower]
                if this_term is not None:
                    try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                        this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                        this_term['hash_docs'].update(hash_temp_doc)
                    except KeyError:
                        print("couldn't update")
                    return  # end of update (1+2)
                else:  # (5) if its a new term (other=PEN and dict='none')
                    nested_hash = ({'tf_c': other_tf_c, 'df': other_df, 'hash_docs': hash_temp_doc})
                    self.hash_file_terms[other_term] = nested_hash
                    return  # end of adding a new term
            else:  # if the current term is lower case 'pen' (if it's an upper case we don't mind)
                if other_term in self.hash_file_terms:  # (3) other=pen and dict=pen -> update
                    this_term = self.hash_file_terms[other_term]
                    try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                        this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                        this_term['hash_docs'].update(hash_temp_doc)
                    except KeyError:
                        print("couldn't update")
                    return  # end of update (3)
                else:  # (4) other=pen and Dict=PEN  -> now will be Dict=pen + update
                    temp_term_upper = other_term.upper()  # temp = PEN
                    if temp_term_upper in self.hash_file_terms:
                        old_term = self.hash_file_terms[temp_term_upper]  # this_term = PEN
                        this_term = copy.deepcopy(old_term)  # creates new lower case term 'pen'
                        try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                            this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'df': this_term['df'] + other_df})
                            this_term['hash_docs'].update(hash_temp_doc)
                        except KeyError:
                            print("couldn't update")
                        self.hash_file_terms[other_term] = this_term  # adds 'pen'
                        del self.hash_file_terms[temp_term_upper]  # deletes old upper case term 'PEN'
                        return  # end of update (4)
                    else:  # (5) if its a new term (other=pen and dict='none')
                        nested_hash = ({'tf_c': other_tf_c, 'df': other_df, 'hash_docs': hash_temp_doc})
                        self.hash_file_terms[other_term] = nested_hash
                        return

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
