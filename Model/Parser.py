import copy
import os
import time
from Model.TermObject import TermObject
from Model.DocObject import DocObject
from Model.CityObject import CityObject
from Model.API import API
from Model.Stemmer import Stemmer


class Parser:

    # initializes strings

    str_doc = ""
    str_doc_id = ""
    str_city_name = ""
    str_txt = ""

    # initializes dictionaries

    hash_terms = {}
    hash_docs = {}
    hash_cities = {}
    hash_stopwords = {}
    hash_keywords_months = {}
    hash_keywords_prices = {}
    hash_punc = {}

    # initializes lists

    list_tokens = []
    list_fractions = []

    # global vars

    global_line_counter = 0  # global line counter in file
    line_in_doc_counter = 0  # global line counter in doc
    word_in_line_counter = 0  # global line word counter in lines

    # constructor #

    def __init__(self):
        project_dir = os.path.dirname(os.path.dirname(__file__))
        str_path_stopwords = 'resources\\stopwords.txt'  # sets stop word dictionary
        str_path_keywords_months = 'resources\\keywords_months.txt'  # sets key word dictionary
        str_path_keywords_prices = 'resources\\keywords_prices.txt'  # sets key word dictionary
        # str_path_test = 'C:\\Users\\edoli\\Desktop\\SE_PA\\test1.txt'
        # self.set_test_file(str_path_test)
        abs_stopword_path = os.path.join(project_dir, str_path_stopwords)
        abs_keyword_path_months = os.path.join(project_dir, str_path_keywords_months)
        abs_keyword_path_prices = os.path.join(project_dir, str_path_keywords_prices)
        self.set_stopwords(abs_stopword_path)  # sets stop word dictionary
        self.set_keywords_months(abs_keyword_path_months)  # sets key word dictionary
        self.set_keywords_prices(abs_keyword_path_prices)  # sets key word dictionary
        self.set_puncwords()  # sets punctuation vocabulary
        self.stemming_mode = False
        if self.stemming_mode:
            self.stemmer = Stemmer()

    # function sets the cities #

    def set_city(self):
        try:
            city_name = self.str_doc.split("<F P=104>")[1]
            city_name = city_name.split("</F>")[0]            
            city_name = city_name.strip()
            l_city = city_name.split(' ')
            if len(l_city) > 1:
                str_city_name1 = l_city[0].upper()
                str_city_name2 = l_city[1].upper()
                str_two_words = str_city_name1 + " " + str_city_name2
                if str_city_name1 not in self.hash_cities:
                    self.hash_cities[str_city_name1] = ""
                if str_two_words not in self.hash_cities:
                    self.hash_cities[str_two_words] = ""
                del str_city_name1
                del str_city_name2
            else:
                str_city_name1 = l_city[0].lower()
                if str_city_name1 not in self.hash_cities:
                    self.hash_cities[str_city_name1] = ""
                del str_city_name1
            self.str_city_name = str_city_name1
            del city_name
            del l_city
        except IndexError:
            a = 0
            # print("marker <F P=104> not found")

    def set_headers(self):
        try:
            str_header = self.str_doc.split("<TI>")[1]
            str_header = str_header.split("</TI>")[0]
            str_header = str_header.strip()
            l_header = str_header.split(' ')
            while len(l_header) > 0:
                term = l_header[0]
                if term not in self.hash_punc and term.lower() not in self.hash_stopwords:
                    self.is_regular_term(term, 1)
                del l_header[0]
        except KeyError:
            a = 0


    # function imports API info #

    def create_api(self):
        obj_api = API(self.hash_cities)
        obj_api.get_api_info()

    # function creates stopword list #

    def set_stopwords(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        list_stopwords = data.split()
        for word in list_stopwords:
            self.hash_stopwords[word] = ""
        del list_stopwords

    # function test #

    def set_test_file(self, file_path):
        with open(file_path, 'r') as file:
            self.str_txt = file.read().replace('\n', ' ')

    # function creates keyword list #

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
        list_punc = {',', '"', '.', '?', '-', '_', '.', '*', '"', '`', ':', ';', "'", '[', ']', '(', ')', '{', "}", '<', '>', '|', '~',
                     '^', '?', "\"", '\"', '&', '"!"', '!', "=", '+', "#", '\n', "\"", '\"', "/", "\\"}
        for word in list_punc:
            self.hash_punc[word] = ""
        del list_punc

    # function prints tokens list #

    def print_list(self):
        print(*self.list_tokens, sep=", ")

    # function prints term dictionary #

    def print_dict(self):
        for key, value in self.hash_terms.items():
            var = "key: ", key, "=>", "value: ", value
            print(var)

    # function counts capitalized letters #

    def count_upper(self, term):
        count = 0
        for ch in term:
            if ch.isupper():
                count += 1
        return count

    # function checks if the first letter of a string is an upper case #

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

    # FORMAT:  DAKAR|{'tf_c': 8192, 'idf': 8192, 'hash_docs': {'FBIS3-638': {'tf_d': 1, 'h': 0}, 'FBIS3-841': {'tf_d': 1, 'h': 0}, 'FBIS3-880': {'tf_d': 1, 'h': 0}, 'FBIS3-884': {'tf_d': 1, 'h': 0}}}
    # FORMAT:  DAKAR|

    def term_case_filter(self, other_term, is_header):
        this_term = None
        if self.stemming_mode:
            other_term = self.stemmer.start_stem(other_term)
        if self.is_first_upper(other_term):  # other = PEN
            if not self.is_fully_upper(other_term):
                other_term = other_term.upper()  # Pen -> PEN
            if other_term in self.hash_terms:  # (1) other=PEN and dict=PEN -> update
                this_term = self.hash_terms[other_term]
            else:  # (2) other=PEN and dict=pen -> update
                temp_term_lower = other_term.lower()  # temp=pen
                if temp_term_lower in self.hash_terms:  # (2) other=PEN and dict=pen -> update
                    this_term = self.hash_terms[temp_term_lower]
            if this_term is not None:
                try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                    this_tf = this_term['hash_docs'][self.str_doc_id]['tf_d'] + 1
                    this_header = this_term['hash_docs'][self.str_doc_id]['h']
                    this_term.update({'tf_c': this_term['tf_c'] + 1})
                    # this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header+is_header, 'pos': "n/a"}})
                    this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header + is_header}})
                    # this_tf = this_term['d'][self.str_doc_id]['d'] + 1
                    # this_header = this_term['d'][self.str_doc_id]['h']
                    # this_term.update({'c': this_term['c'] + 1})
                    # this_term['d'].update({self.str_doc_id: {'d': this_tf, 'h': this_header + is_header}})
                    if this_tf == 2:
                        this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                        self.hash_docs[self.str_doc_id]['unique_count'] = this_unique - 1
                except KeyError:  # if it's the first occurrence in this new doc -> we update tf_c, df, tf_d and pos
                    this_tf = 1  # new doc therefore new value for tf_d and added to existing tf_c
                    this_term.update({'tf_c': this_term['tf_c'] + this_tf, 'df': this_term['df'] + 1})
                    # this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header, 'pos': "n/a"}})
                    this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header}})
                    this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                    self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                if this_tf > self.hash_docs[self.str_doc_id]['max_tf']:  # update max tf
                    self.hash_docs[self.str_doc_id]['max_tf'] = this_tf
                # new_pos = ['(' + str(self.line_in_doc_counter) + ',' + str(self.word_in_line_counter) + ')']
                # this_term[self.hash_docs][self.str_doc_id][pos] = list_pos.append(new_pos)
                return  # end of update (1+2)
            else:  # (5) if its a new term (other=PEN and dict='none')
                # list_term_pos = ['(' + str(self.line_in_doc_counter) + ',' + str(self.word_in_line_counter) + ')']
                # nested_hash = ({'tf_c': 1, 'df': 1, 'hash_docs': {self.str_doc_id: {'tf_d': 1, 'pos': list_term_pos}}})
                # nested_hash = ({'tf_c': 1, 'df': 1, 'hash_docs': {self.str_doc_id: {'tf_d': 1, 'h': is_header, 'pos': "n/a"}}})
                nested_hash = ({'tf_c': 1, 'df': 1, 'hash_docs': {self.str_doc_id: {'tf_d': 1, 'h': is_header}}})
                self.hash_terms[other_term] = nested_hash
                this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                return  # end of adding a new term
        else:  # if the current term is lower case 'pen' (if it's an upper case we don't mind)
            if other_term in self.hash_terms:  # (3) other=pen and dict=pen -> update
                this_term = self.hash_terms[other_term]
                try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                    this_tf = this_term['hash_docs'][self.str_doc_id]['tf_d'] + 1
                    this_header = this_term['hash_docs'][self.str_doc_id]['h']
                    this_term.update({'tf_c': this_term['tf_c'] + 1})
                    # this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header+is_header, 'pos': "n/a"}})
                    this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header + is_header}})
                    if this_tf == 2:
                        this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                        self.hash_docs[self.str_doc_id]['unique_count'] = this_unique - 1
                except KeyError:  # if it's the first occurrence in this new doc -> we update tf_c, df, tf_d and pos
                    this_tf = 1  # new doc therefore new value for tf_d and added to existing tf_c
                    this_term.update({'tf_c': this_term['tf_c'] + this_tf, 'df': this_term['df'] + 1})
                    # this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header, 'pos': "n/a"}})
                    this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header}})
                    this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                    self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                if this_tf > self.hash_docs[self.str_doc_id]['max_tf']:  # update max tf
                    self.hash_docs[self.str_doc_id]['max_tf'] = this_tf
                # new_pos = ['(' + str(self.line_in_doc_counter) + ',' + str(self.word_in_line_counter) + ')']
                # this_term[self.hash_docs][self.str_doc_id][pos] = list_pos.append(new_pos)
                return  # end of update (3)
            else:  # (4) other=pen and Dict=PEN  -> now will be Dict=pen + update
                temp_term_upper = other_term.upper()  # temp = PEN
                if temp_term_upper in self.hash_terms:
                    old_term = self.hash_terms[temp_term_upper]  # this_term = PEN
                    this_term = copy.deepcopy(old_term)  # creates new lower case term 'pen'
                    try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                        this_tf = this_term['hash_docs'][self.str_doc_id]['tf_d'] + 1
                        this_header = this_term['hash_docs'][self.str_doc_id]['h']
                        this_term.update({'tf_c': this_term['tf_c'] + 1})
                        # this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header+is_header, 'pos': "n/a"}})
                        this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header + is_header}})
                        if this_tf == 2:
                            this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                            self.hash_docs[self.str_doc_id]['unique_count'] = this_unique - 1
                    except KeyError:  # if it's the first occurrence in this new doc -> we update tf_c, df, tf_d and pos
                        this_tf = 1  # new doc therefore new value for tf_d and added to existing tf_c
                        this_term.update({'tf_c': this_term['tf_c'] + this_tf, 'df': this_term['df'] + 1})
                        # this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header, 'pos': "n/a"}})
                        this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header}})
                        this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                        self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                    if this_tf > self.hash_docs[self.str_doc_id]['max_tf']:  # update max tf
                        self.hash_docs[self.str_doc_id]['max_tf'] = this_tf
                    # new_pos = ['(' + str(self.line_in_doc_counter) + ',' + str(self.word_in_line_counter) + ')']
                    # this_term[self.hash_docs][self.str_doc_id][pos] = list_pos.append(new_pos)
                    self.hash_terms[other_term] = this_term  # adds 'pen'
                    del self.hash_terms[temp_term_upper]  # deletes old upper case term 'PEN'
                    return  # end of update (4)
                else:  # (5) if its a new term (other=pen and dict='none')
                    # list_term_pos = ['(' + str(self.line_in_doc_counter) + ',' + str(self.word_in_line_counter) + ')']
                    # nested_hash = ({'tf_c': 1, 'df': 1, 'hash_docs': {self.str_doc_id: {'tf_d': 1, 'pos': list_term_pos}}})
                    # nested_hash = ({'tf_c': 1, 'df': 1, 'hash_docs': {self.str_doc_id: {'tf_d': 1, 'h': is_header, 'pos': "n/a"}}})
                    nested_hash = ({'tf_c': 1, 'df': 1, 'hash_docs': {self.str_doc_id: {'tf_d': 1, 'h': is_header}}})
                    self.hash_terms[other_term] = nested_hash
                    this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                    self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                    return

    def make_upper_case(self, term):
        i = 0
        word = term
        for ch in word:
            if 96 < ord(ch) < 123:
                word = word[:i] + chr(ord(ch) - 32) + word[i + 1:]
            i += 1
        return word

    def make_lower_case(self, term):
        i = 0
        word = term
        for ch in word:
            if 64 < ord(ch) < 91:
                word = word[:i] + chr(ord(ch) + 32) + word[i + 1:]
            i += 1
        return word

    # function filters regular terms #

    def is_regular_term(self, term, is_header):  # Note: "/F", "Type:BN", "equipment,", "March]", "approval/disapproval"
        if term != "-" and term != '':
            size = len(term) - 1
            last = term[size]
            first = term[0]  # "term-", "term--"
            while ((size > 0 and last != '') and (last in self.hash_punc or '\"' in last or "\\" in last)):
                term = term[:-1]
                size -= 1
                if size > 0:
                    last = term[size]
            while ((size > 0 and first != '') and (first in self.hash_punc or '\"' in first or "\\" in first)):
                term = term[1:]
                size -= 1
                if size > 0:
                    first = term[0]
            if "@" in term:  # '@' our new rule
                list_mail = term.split('@')
                if list_mail[0]:
                    self.term_case_filter(list_mail[0], is_header)
                if list_mail[1]:
                    self.term_case_filter(list_mail[1], is_header)
                del list_mail
            if term != '' and term != '%' and ')' not in term and ']' not in term and '\"' not in term and "\\" not in term and term not in self.hash_punc:
                term = term.strip()
                self.term_case_filter(term, is_header)

    # prevent index increment if double delete
    two_deleted = 0

    def convert_numbers_in_list(self, index):
        list_t = self.list_tokens
        tmp_term = list_t[index]
        term_size = len(tmp_term)
        while tmp_term[term_size-1] in self.hash_punc:
            tmp_term = tmp_term[:-1]
            term_size -=1
        list_t[index] = tmp_term
        # first loop correct number forms
        operation_done = 0
        term = list_t[index]
        dot_pos = term.find('.')
        if dot_pos == len(term) - 1:
            term = term.replace('.', '')
        if '/' not in term and '-' not in term:
            if not self.is_year(index):
                if '$' not in term and 'bn' not in term and 'm' not in term:
                    try:
                        float(term)
                        self.list_tokens[index] = self.numbers_rules(term)
                    except ValueError:
                        #print("the argument : | " + self.list_tokens[index] + " | could not be parsed")
                        return 'SyntaxError{}'
            else:
                self.edit_list_by_key_word_dates(index)
                operation_done = 1
            if operation_done == 0:
                try:
                    ans = self.edit_list_by_key_word_prices(index)
                    # if self.two_deleted == 1:
                    # self.two_deleted = 0
                    # index -= 1
                    return ans
                except ValueError:
                   # print("the argument : | " + self.list_tokens[index] + " | could not be parsed")
                    return 'SyntaxError{}'
        elif '/' in term:
            nums_in_fraction = term.split('/', 1)
            numerator = nums_in_fraction[0]
            denominator = nums_in_fraction[1]
            numerator = self.numbers_rules(numerator)
            denominator = self.numbers_rules(denominator)
            self.list_tokens[index] = numerator + '/' + denominator
            if index > 0 and '/' not in self.list_tokens[index - 1]:
                if self.is_number(self.list_tokens[index - 1]):
                    to_add = self.is_fraction(index)
                    self.list_tokens[index] = to_add
        return self.list_tokens[index]

    def is_number(self, term):
        term.replace('.', '')
        contain_special = False
        all_numbers = all(char.isdigit() for char in term)
        if not all_numbers:
            try:
                temp_term = list(term)
                first_char = temp_term[0]
                last_char = temp_term[-1:]
                last_two_chars = temp_term[-2:]
                if first_char == '$':
                    contain_special = True
                elif last_two_chars == 'bn' or last_two_chars == 'Bn' or last_char == 'm' or last_char == 'M':
                    has_numbers = any(char.isdigit() for char in term)
                    if has_numbers == True:
                        contain_special = True
            except IndexError:
                print("index out of bound in: @ is_number")
        ans = all_numbers or contain_special
        return ans

    # convert number term according to rules

    def numbers_rules(self, num_str):
        # num_edit = num_str.replace(",", "")
        number_split = num_str.split(".", 1)
        before_point = number_split[0]
        if len(number_split) > 1:
            after_point = number_split[1]
        else:
            after_point = ''
        if len(before_point) > 12:
            ans = self.format_num(before_point + '000', 'B', 12, after_point)
        elif len(before_point) > 9:
            ans = self.format_num(before_point, 'B', 9, after_point)
        elif len(before_point) > 6:
            ans = self.format_num(before_point, 'M', 6, after_point)
        elif len(before_point) > 3:
            ans = self.format_num(before_point, 'K', 3, after_point)
        else:
            if after_point != '':
                ans = before_point + '.' + after_point
            else:
                ans = before_point
        dot_pos = ans.find('.')
        if dot_pos != -1:
            if ans[dot_pos + 1] == 'K' or ans[dot_pos + 1] == 'M' or ans[dot_pos + 1] == 'B':
                ans = list(ans)
                del ans[dot_pos]
                ans = "".join(ans)
        return ans

    '''this function formats big numbers acording to rules'''

    def format_num(self, number, sign, mode, after_point):
        zero_killer = 1
        num_desired_format = number[:-mode] + '.' + number[-mode:]
        num_desired_format = list(num_desired_format)
        while num_desired_format[len(num_desired_format) - zero_killer] == '0' and after_point == '':
            num_desired_format[len(num_desired_format) - zero_killer] = ''
            zero_killer = zero_killer + 1
        num_desired_format = "".join(num_desired_format)
        return num_desired_format + after_point + sign

    def format_num_dollar_mode(self, number):
        multy = 0
        if '$' in number:
            number = number.replace('$', '')
        if 'O' in number:
            number = number.replace('O', '0')
        num_desired_format = number
        if 'K' in number:
            multy = 1000
            number = number.replace('K', '')
            number = str(float(number) / multy)
        elif 'M' in number:
            multy = 1
            number = number.replace('M', '')
            number = str(float(number) * multy)
        elif 'B' in number:
            multy = 1000
            number = number.replace('B', '')
            number = str(float(number) * multy)
        if (float(number)) > 1000:
            num_desired_format = number.replace('.', '')
        return '$' + num_desired_format + 'M'

    def edit_list_by_key_word_prices(self, index):
        term_prev = ""
        term_next = ""
        term_next_next = ""
        ans = ""
        need_to_update = 0
        index_front = 0
        index_back = 0
        operation_done = 0
        if index > 0:
            index_back = self.ignore_asterisk_back_mode(index)
            term_prev = self.list_tokens[index_back]
        term_current = self.list_tokens[index]
        temp_term = list(term_current)
        if index < len(self.list_tokens) - 1:
            index_front = self.ignore_asterisk_front_mode(index)
            term_next = self.list_tokens[index_front]
        if index < len(self.list_tokens) - 2:
            term_next_next = self.list_tokens[index + 2]
        if 'm' in temp_term:
            temp_term[temp_term.index('m')] = 'M'
            term_current = "".join(temp_term)
        elif term_current.find('b') != -1:
            if temp_term[0] == '$':
                term_current = term_current.replace('$', '')
            b_index = temp_term.index('b') - 1
            float_num = float(term_current[:b_index]) * 1000
            if float_num.is_integer():
                float_num = int(float_num)
            if temp_term[0] == '$':
                temp_term = '$' + str(float_num)
            else:
                temp_term = str(float_num)
            term_current = temp_term + 'M'
        elif term_next != "" and term_next == '%' or term_next == 'percent' or term_next == 'percentage':
            ans = self.num_percent(term_current)
            self.list_tokens[index] = ans
            del self.list_tokens[index + 1]
        elif term_next != "" and term_next == 'Thousand' or term_next == 'Million' or term_next == 'Billion' \
                or term_next == 'Trillion' or term_next == 'million' or term_next == 'billion' \
                or term_next == 'trillion' or term_next == 'thousand':
            if '$' in term_current:
                if term_next == 'Thousand' or term_next == 'thousand':
                    ans = self.format_num_dollar_mode(str(float(term_current) / 1000))
                elif term_next == 'Million' or term_next == 'million':
                    ans = self.format_num_dollar_mode(term_current)
                elif term_next == 'Billion' or term_next == 'billion':
                    ans = self.format_num_dollar_mode(term_current + '000')
                elif term_next == 'Trillion' or term_next == 'trillion':
                    ans = self.format_num_dollar_mode(term_current + '000000')
            elif term_next_next != "" and term_next_next == 'U.S.':
                if term_next == 'Thousand' or term_next == 'thousand':
                    ans = self.format_num_dollar_mode(str(float(term_current) / 1000))
                if term_next == 'Million' or term_next == 'million':
                    ans = self.format_num_dollar_mode(term_current)
                if term_next == 'Billion' or term_next == 'billion':
                    ans = self.format_num_dollar_mode(term_current + '000')
                if term_next == 'Trillion' or term_next == 'trillion':
                    ans = self.format_num_dollar_mode(term_current + '000000')
                need_to_update = 1
                operation_done = 1
            else:
                if term_next == 'Thousand' or term_next == 'thousand':
                    ans = self.format_num(term_current, 'K', 3, '')
                if term_next == 'Million' or term_next == 'million':
                    ans = self.format_num(term_current, 'M', 6, '')
                if term_next == 'Billion' or term_next == 'Trillion' or term_next == 'billion' or term_next == 'trillion':
                    ans = self.format_num(term_current, 'B', 9, '')
            # self.list_tokens[index] = ans
            term_current = ans
            # del self.list_tokens[index_front]
            # self.two_deleted = 1
            if index < len(self.list_tokens) and need_to_update == 1:
                term_next = self.list_tokens[index_front]
        if term_current == 'm' or term_current == 'bn' and operation_done == 0:
            if term_current == 'm':
                ans = self.format_num(term_prev, 'M', 6, '')
                # self.list_tokens[index] = ans
                # del self.list_tokens[index_back]
            if term_current == 'bn':
                ans = self.format_num_dollar_mode(term_prev, 'M')
                # term_current = ans
                # self.list_tokens[index] = ans
                # del self.list_tokens[index_back]
                index -= 1
        if term_next != "" and term_next == 'Dollars' or term_next == 'dollars':
            ans = self.num_dollar(term_current)
            # self.list_tokens[index] = ans
            # del self.list_tokens[index_front]
        if term_prev != "" and term_prev == '$':
            ans = self.num_dollar(term_current)
            # self.list_tokens[index] = ans
            del self.list_tokens[index_back]
        if '$' in term_current:
            term_current = term_current.replace('$', '')
            ans = self.num_dollar(term_current)
            # self.list_tokens[index] = ans
        return ans

    def edit_list_by_key_word_dates(self, index):
        term_prev = ""
        term_next = ""
        ans = ""
        month_num = '0'
        index_back = 0
        index_front = 0
        term_current = self.list_tokens[index]
        if index > 0:
            index_back = self.ignore_asterisk_back_mode(index)
            term_prev = self.list_tokens[index_back]
        if index < len(self.list_tokens) - 1:
            index_front = self.ignore_asterisk_front_mode(index)
            term_next = self.list_tokens[index_front]
        if term_current == 'Jan' or term_current == 'JAN' or term_current == 'January' or term_current == 'JANUARY':
            month_num = '01'
        elif term_current == 'Feb' or term_current == 'FEB' or term_current == 'February' or term_current == 'FEBRUARY':
            month_num = '02'
        elif term_current == 'Mar' or term_current == 'MAR' or term_current == 'March' or term_current == 'MARCH':
            month_num = '03'
        elif term_current == 'Apr' or term_current == 'apr' or term_current == 'April' or term_current == 'APRIL':
            month_num = '04'
        elif term_current == 'May' or term_current == 'MAY':
            month_num = '05'
        elif term_current == 'Jun' or term_current == 'JUN' or term_current == 'June' or term_current == 'JUNE':
            month_num = '06'
        elif term_current == 'Jul' or term_current == 'JUL' or term_current == 'July' or term_current == 'JULY':
            month_num = '07'
        elif term_current == 'Aug' or term_current == 'AUG' or term_current == 'August' or term_current == 'AUGUST':
            month_num = '08'
        elif term_current == 'Sep' or term_current == 'SEP' or term_current == 'September' or term_current == 'SEPTEMBER':
            month_num = '09'
        elif term_current == 'Oct' or term_current == 'OCT' or term_current == 'October' or term_current == 'OCTOBER':
            month_num = '10'
        elif term_current == 'Nov' or term_current == 'NOV' or term_current == 'November' or term_current == 'NOVEMBER':
            month_num = '11'
        elif term_current == 'Dec' or term_current == 'DEC' or term_current == 'December' or term_current == 'DECEMBER':
            month_num = '12'
        if month_num != '0':
            if self.represents_int(term_prev):
                if len(term_prev) == 1:
                    term_prev = '0' + term_prev
                if len(term_prev) > 2:
                    ans = term_prev + '-' + month_num
                else:
                    ans = month_num + '-' + term_prev
                self.list_tokens[index] = ans
                del self.list_tokens[index_back]
            elif self.represents_int(term_next):
                if len(term_next) == 1:
                    term_next = '0' + term_next
                if len(term_next) > 2:
                    ans = term_next + '-' + month_num
                else:
                    ans = month_num + '-' + term_next
                del self.list_tokens[index_front]
                self.list_tokens[index] = ans

    def is_year(self, index):
        term_prev = ""
        term_next = ""
        if index > 0:
            index_back = self.ignore_asterisk_back_mode(index)
            term_prev = self.list_tokens[index_back]
        if index < len(self.list_tokens) - 1:
            index_front = self.ignore_asterisk_front_mode(index)
            term_next = self.list_tokens[index_front]
        if term_next in self.hash_keywords_months or term_prev in self.hash_keywords_months:
            return True
        return False

    def ignore_asterisk_back_mode(self, index):
        index -= 1
        while index > 0 and self.list_tokens[index] == '*':
            index -= 1
        return index

    def ignore_asterisk_front_mode(self, index):
        index += 1
        while index < len(self.list_tokens) - 2 and self.list_tokens[index] == '*':
            index += 1
        return index

    def is_fraction(self, index):
        to_add = ""
        if index < len(self.list_tokens):
            to_add = self.list_tokens[index - 1] + ' ' + self.list_tokens[index]
            del self.list_tokens[index - 1]
        return to_add

    def num_percent(self, number):
        return number + "%"

    def num_dollar(self, number):
        return number + " Dollars"

    # check if string represents int
    def represents_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    # add city line numbers

    def city_lines_and_docs(self):
        self.line_counter = self.line_counter + self.str_doc.count('\n')

    # function filters all terms #

    def start_parse(self, str_doc):
        # self.hash_terms = {}
        if str_doc:  # sets current document
            self.str_doc = str_doc
        try:
            self.str_doc_id = (self.str_doc.split("</DOCNO>", 1)[0]).split("<DOCNO>")[1].strip()
        except AttributeError:
            pass
        try:
            self.str_txt = self.str_doc.split("<TEXT>")[1].strip()
            self.str_txt = self.str_txt.split("</TEXT>")
            self.str_txt = self.str_txt[0]
        except (IndexError, AttributeError) as e:
            pass
        self.str_txt = self.str_txt.replace('*', '')
        self.str_txt = self.str_txt.replace('\n', ' * ')
        self.list_tokens = self.str_txt.split()
        # self.convert_numbers_in_list()
        index = 0
        self.hash_docs.update({self.str_doc_id: {'max_tf': 0, 'unique_count': 0, 'doc_size': len(self.list_tokens), 'city_origin': self.str_city_name}})
        #self.set_city()
        self.set_headers()
        del self.str_doc
        del self.str_txt
        for term in self.list_tokens:
            if term != '':
                if term == '*':
                    self.line_in_doc_counter += 1
                    self.global_line_counter += 1
                    self.word_in_line_counter = 0
                else:
                    if ',' in term:
                        term = term.replace(',', '')
                        self.list_tokens[index] = term
                    if term and term not in self.hash_punc and term not in self.hash_stopwords:
                        try:
                            if term[0].isdigit() or term[0] == '$':
                                term = self.convert_numbers_in_list(index)
                                if term == 'SyntaxError{}':
                                    term = self.list_tokens[index]
                                    # print('Term| ' +term+' |inserted.')
                        except IndexError:
                            print('dickTerm: ' + term)
                        if term != "-" and term!= "--" and term != '':
                            hyphen_term = term
                            if "--" in term:  # term1--term2
                                list_double = term.split('--')
                                if list_double[0] != "":
                                    self.is_regular_term(list_double[0], 0)
                                if list_double[1] != "":
                                    self.is_regular_term(list_double[1], 0)
                                del list_double
                            elif "-" in term:  # term1-term2-term3
                                word_split = []
                                while "-" in hyphen_term:
                                    word_split = hyphen_term.rstrip().split('-', 1)
                                    term1 = word_split[0]
                                    if term1 != '':
                                        self.is_regular_term(term1, 0)
                                    word_split.remove(term1)
                                    hyphen_term = word_split[0]
                                    if hyphen_term != '':
                                        self.is_regular_term(term, 0)
                                del word_split
                            self.is_regular_term(term, 0)
                            self.word_in_line_counter += 1

                index += 1


        # return self.hash_terms
        # print("done")

        '''  self.convert_numbers_in_list()
                   for term in self.list_tokens_second_pass:
                       if '-' in term:
                           self.is_hyphen_number_mode(term)
                       else:
                           self.add_term_number_mode(term)'''
