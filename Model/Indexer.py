import collections
import os


class Indexer:

    def __init__(self, user_path):
        posting_path = user_path + "/temp_files/"
        if not os.path.exists(posting_path):
            os.makedirs(posting_path)
        self.file_path0 = posting_path + 'int.txt'
        self.file_path1 = posting_path + 'abc.txt'
        self.file_path2 = posting_path + 'defgh.txt'
        self.file_path3 = posting_path + 'ijklm.txt'
        self.file_path4 = posting_path + 'nopq.txt'
        self.file_path5 = posting_path + 'rstu.txt'
        self.file_path6 = posting_path + 'vxwyz.txt'

    def update_files(self, hash_terms):
        hash_terms = collections.OrderedDict(sorted(hash_terms.items()))
        with open(self.file_path0, 'a', encoding='utf-8') as int:
            with open(self.file_path1, 'a', encoding='utf-8') as abc:
                with open(self.file_path2, 'a', encoding='utf-8') as defgh:
                    with open(self.file_path3, 'a', encoding='utf-8') as ijklm:
                        with open(self.file_path4, 'a', encoding='utf-8') as nopq:
                            with open(self.file_path5, 'a', encoding='utf-8') as rstu:
                                with open(self.file_path6, 'a', encoding='utf-8') as vwxyz:
                                    flag_int = True
                                    for key, value in hash_terms.items():
                                        if flag_int and self.is_number(key):
                                            int.write(str(key) + "|" + str(value) + '\n')
                                        else:
                                            flag_int = False
                                            ch = ord(key[0])
                                            if 97 <= ch <= 99 or 65 <= ch <= 67:
                                                abc.write(str(key) + "|" + str(value) + '\n')
                                            elif 100 <= ch <= 104 or 68 <= ch <= 72:
                                                defgh.write(str(key) + "|" + str(value) + '\n')
                                            elif 105 <= ch <= 109 or 73 <= ch <= 77:
                                                ijklm.write(str(key) + "|" + str(value) + '\n')
                                            elif 110 <= ch <= 113 or 78 <= ch <= 81:
                                                nopq.write(str(key) + "|" + str(value) + '\n')
                                            elif 114 <= ch <= 117 or 82 <= ch <= 85:
                                                rstu.write(str(key) + "|" + str(value) + '\n')
                                            elif 118 <= ch <= 122 or 86 <= ch <= 90:
                                                vwxyz.write(str(key) + "|" + str(value) + '\n')
                                    vwxyz.close()
                                rstu.close()
                            nopq.close()
                        ijklm.close()
                    defgh.close()
                abc.close()
            int.close()

    def is_number(self, term):
        return term[0].isdigit()
