import os
import copy
import shutil
from multiprocessing import Pool, Lock


m_arr = [Lock(), Lock(), Lock(), Lock(), Lock(), Lock(), Lock()]


class Indexer:

    def __init__(self, user_path):
        self.posting_path = user_path + "/temp_files/"
        if not os.path.exists(self.posting_path):
            os.makedirs(self.posting_path)
        self.file_path0 = self.posting_path + 'int.txt'
        self.file_path1 = self.posting_path + 'abc.txt'
        self.file_path2 = self.posting_path + 'defgh.txt'
        self.file_path3 = self.posting_path + 'ijklm.txt'
        self.file_path4 = self.posting_path + 'nopq.txt'
        self.file_path5 = self.posting_path + 'rstu.txt'
        self.file_path6 = self.posting_path + 'vxwyz.txt'
        self.hash_file_terms = {}
        self.counter = 0

    def write_temp_posts(self, hash_terms):
        hash_terms = sorted(hash_terms.items(), key=lambda x: x[0].lower())
        m_arr[0].acquire()
        with open(self.file_path0, 'a', encoding='utf-8') as int:
            i = 0
            for key, value in hash_terms:
                if key[0].isdigit():
                    int.write(str(key) + "|" + str(value) + '\n')
                    i += 1
                else:
                    break
            for x in range(0, i):
                del hash_terms[0]
            int.close()
        m_arr[0].release()
        m_arr[1].acquire()
        with open(self.file_path1, 'a', encoding='utf-8') as abc:
            i = 0
            for key, value in hash_terms:
                ch = ord(key[0])
                if 97 <= ch <= 99 or 65 <= ch <= 67:
                    abc.write(str(key) + "|" + str(value) + '\n')
                    i += 1
                else:
                    break
            for x in range(0, i):
                del hash_terms[0]
            abc.close()
        m_arr[1].release()
        m_arr[2].acquire()
        with open(self.file_path2, 'a', encoding='utf-8') as defgh:
            i = 0
            for key, value in hash_terms:
                ch = ord(key[0])
                if 100 <= ch <= 104 or 68 <= ch <= 72:
                    defgh.write(str(key) + "|" + str(value) + '\n')
                    i += 1
                else:
                    break
            for x in range(0, i):
                del hash_terms[0]
            defgh.close()
        m_arr[2].release()
        m_arr[3].acquire()
        with open(self.file_path3, 'a', encoding='utf-8') as ijklm:
            i = 0
            for key, value in hash_terms:
                ch = ord(key[0])
                if 105 <= ch <= 109 or 73 <= ch <= 77:
                    ijklm.write(str(key) + "|" + str(value) + '\n')
                    i += 1
                else:
                    break
            for x in range(0, i):
                del hash_terms[0]
            ijklm.close()
        m_arr[3].release()
        m_arr[4].acquire()
        with open(self.file_path4, 'a', encoding='utf-8') as nopq:
            i = 0
            for key, value in hash_terms:
                ch = ord(key[0])
                if 110 <= ch <= 113 or 78 <= ch <= 81:
                    nopq.write(str(key) + "|" + str(value) + '\n')
                    i += 1
                else:
                    break
            for x in range(0, i):
                del hash_terms[0]
            nopq.close()
        m_arr[4].release()
        m_arr[5].acquire()
        with open(self.file_path5, 'a', encoding='utf-8') as rstu:
            i = 0
            for key, value in hash_terms:
                ch = ord(key[0])
                if 114 <= ch <= 117 or 82 <= ch <= 85:
                    rstu.write(str(key) + "|" + str(value) + '\n')
                    i += 1
                else:
                    break
            for x in range(0, i):
                del hash_terms[0]
            rstu.close()
        m_arr[5].release()
        m_arr[6].acquire()
        with open(self.file_path6, 'a', encoding='utf-8') as vwxyz:
            i = 0
            for key, value in hash_terms:
                ch = ord(key[0])
                if 118 <= ch <= 122 or 86 <= ch <= 90:
                    vwxyz.write(str(key) + "|" + str(value) + '\n')
                    i += 1
                else:
                    break
                for x in range(0, i):
                    del hash_terms[0]
            vwxyz.close()
        m_arr[6].release()

        # self.counter += 1
        # if self.counter == 5:
        #     self.sort_file_list(self.file_path1)
        # self.sort_file_hash(self.file_path1)
        # self.sort_file_list(self.file_path1)

    def sort_file_hash(self, file_name):
        hash_terms = {}
        with open(file_name, 'a', encoding='utf-8') as file:
            for line in file_name:
                (key, val) = line.split()
                self.hash_file_terms[int(key)] = val
            file.close()
        for term in hash_terms:
            self.merger(term)
        self.write_temp_posts(self.hash_file_terms)

    def sort_file_list(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            list_terms = [line.strip() for line in file]
            file.close()
        for term in list_terms:
            term = term.split('|')
            self.merger(term)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.close()
        self.write_temp_posts(self.hash_file_terms)

    def merger(self, list_term):
        this_term = None
        other_term = list_term[0]
        if other_term != '':
            value_term = list_term[1].split(',')
            get_tf_c = value_term[0].split(':')
            other_tf_c = int(get_tf_c[1])
            get_idf = value_term[1].split(':')
            other_idf = int(get_idf[1])
            del value_term[0]
            del value_term[0]
            del get_tf_c
            del get_idf
            hash_temp_doc = {}
            get_hash_doc = value_term[0].split(':')
            other_doc_id = get_hash_doc[1]
            other_doc_id = other_doc_id[3:-1]
            other_tf_d = int(get_hash_doc[3])
            get_header = value_term[1].split(': ')
            other_header = int(get_header[1])
            get_pos = value_term[2].split(':')
            other_pos = get_pos[1]
            other_pos = other_pos[2:-2]
            last = len(other_pos)-1
            if other_pos[last] == '}':
                other_pos = other_pos[0:-2]
            hash_temp_doc.update({other_doc_id: {'tf_d': other_tf_d, 'is_header': other_header, 'pos': other_pos}})
            del get_hash_doc
            del get_header
            del get_pos
            del value_term[0]
            del value_term[0]
            del value_term[0]
            while len(value_term) != 0:
                get_hash_doc = value_term[0].split(':')
                other_doc_id = get_hash_doc[0]
                other_doc_id = other_doc_id[2:-1]
                other_tf_d = int(get_hash_doc[2])
                get_header = value_term[1].split(': ')
                other_header = int(get_header[1])
                get_pos = value_term[2].split(':')
                other_pos = get_pos[1]
                other_pos = other_pos[2:-2]
                last = len(other_pos)-1
                if other_pos[last] == '}':
                    other_pos = other_pos[0:-2]
                hash_temp_doc.update({other_doc_id: {'tf_d': other_tf_d, 'is_header': other_header, 'pos': other_pos}})
                del get_hash_doc
                del get_pos
                del value_term[0]
                del value_term[0]
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
                        this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'idf': this_term['idf'] + other_idf})
                        this_term['hash_docs'].update(hash_temp_doc)
                    except KeyError:
                        print("couldn't update")
                    return  # end of update (1+2)
                else:  # (5) if its a new term (other=PEN and dict='none')
                    nested_hash = ({'tf_c': other_tf_c, 'idf': other_idf, 'hash_docs': hash_temp_doc})
                    self.hash_file_terms[other_term] = nested_hash
                    return  # end of adding a new term
            else:  # if the current term is lower case 'pen' (if it's an upper case we don't mind)
                if other_term in self.hash_file_terms:  # (3) other=pen and dict=pen -> update
                    this_term = self.hash_file_terms[other_term]
                    try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                        this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'idf': this_term['idf'] + other_idf})
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
                            this_term.update({'tf_c': this_term['tf_c'] + other_tf_c, 'idf': this_term['idf'] + other_idf})
                            this_term['hash_docs'].update(hash_temp_doc)
                        except KeyError:
                            print("couldn't update")
                        self.hash_file_terms[other_term] = this_term  # adds 'pen'
                        del self.hash_file_terms[temp_term_upper]  # deletes old upper case term 'PEN'
                        return  # end of update (4)
                    else:  # (5) if its a new term (other=pen and dict='none')
                        nested_hash = ({'tf_c': other_tf_c, 'idf': other_idf, 'hash_docs': hash_temp_doc})
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

