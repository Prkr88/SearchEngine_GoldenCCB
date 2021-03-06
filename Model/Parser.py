import copy
from nltk.stem.snowball import EnglishStemmer
from random import randint


########################################################################################################################
# Class Parser:                                                                                                        #
#                                                                                                                      #
# Initialized every file. Receives document and returns a dictionary of tokens.                                        #
########################################################################################################################


class Parser:

    # initializes strings

    str_doc = ""
    str_doc_id = ""
    str_qry_id = ""
    str_city_name = ""
    str_txt = ""

    # initializes dictionaries

    hash_terms = {}  # hash dictionary of terms
    hash_docs = {}  # hash dictionary of documents
    hash_cities = {}  # hash dictionary of cities
    hash_stopwords = {}  # hash dictionary of stopwords
    hash_keywords_months = {}  # hash dictionary of months
    hash_keywords_prices = {}  # hash dictionary of prices
    hash_punc_middle = {}  # hash dictionary of punctuations
    hash_punc = {}  # hash dictionary of punctuations
    hash_stemmer = {}  # hash dictionary of stemmed terms
    hash_alphabet = {}  # hash dictionary of the alphabet
    hash_header = {}  # hash dictionary of header terms
    hash_qry_stopwords = {}  # hash dictionary of query stopwords
    hash_titles = {}

    # initializes lists

    list_tokens = []  # list of the documents' tokens
    list_fractions = []  # list of the documents' fractions

    # global vars

    global_line_counter = 0  # global line counter in file
    line_in_doc_counter = 0  # global line counter in doc
    word_in_line_counter = 0  # global line word counter in lines
    doc_counter = 0           # counts docs in file

    # constructor #

    def __init__(self, hash_stopwords, hash_keywords_months, hash_keywords_prices, hash_punc, hash_punc_middle, hash_alphabet, stemmer, hash_qry_stopwords):
        self.hash_terms = {}
        self.hash_docs = {}
        self.hash_cities = {}
        self.hash_titles = {}
        self.hash_stopwords = hash_stopwords
        self.hash_keywords_months = hash_keywords_months
        self.hash_keywords_prices = hash_keywords_prices
        self.hash_punc = hash_punc
        self.hash_punc_middle = hash_punc_middle
        self.hash_headers = {}
        self.hash_alphabet = hash_alphabet
        self.hash_qry_stopwords = hash_qry_stopwords
        self.stemming_mode = stemmer
        if self.stemming_mode:
            self.stemmer = EnglishStemmer()
        else:
            self.stemmer = None
        self.str_txt_title = ''
        self.str_txt_desc = ''
        self.str_txt_narr = ''

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
                    self.hash_cities.update({str_city_name1: {self.str_doc_id: "(FP=104)"}})
                if str_two_words not in self.hash_cities:
                    self.hash_cities.update({str_two_words: {self.str_doc_id: "(FP=104)"}})
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
        except Exception:
            a = 0

    # function sets header terms (our rule) #

    def set_headers(self):
        self.hash_headers = {}
        str_header = ''
        l_header = None
        self.hash_headers = {}
        skip1 = False
        skip2 = False
        try:
            str_header = self.str_doc.split("<TI>")[1]
            str_header = str_header.split("</TI>")[0]
            str_header = str_header.strip()
            l_header = str_header.split(' ')
        except Exception:
            skip1 = True
        try:
            str_header = self.str_doc.split("<HEADLINE>")[1]
            str_header = str_header.split("</HEADLINE>")[0]
            str_header = str_header.strip()
            l_header = str_header.split(' ')
        except Exception:
            skip2 = True
        try:
            if (not skip1 or not skip2) and str_header != '' and l_header is not None:
                for value in l_header:
                    self.hash_headers[value] = ""
                self.list_tokens.extend(l_header)
        except Exception:
            a = 0

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
        except Exception:
            pass

    # function checks if the first letter  and the second of a string is an upper case #

    def is_fully_upper(self, term):
        if len(term) > 1:
            return 64 < ord(term[0]) < 91 and 64 < ord(term[1]) < 91
        else:
            return 64 < ord(term[0]) < 91

    # main function receives a token term and inserts it appropriately to the set of hash terms #

    def term_case_filter(self, other_term, is_doc):
        try:
            if self.clean_term(other_term, is_doc) and self.valid_range(other_term) and '|' not in other_term:
                this_term = None
                if self.stemming_mode:
                    if other_term not in self.hash_stemmer:  # (1) new 'cars' or 'car'
                        other_term = self.stemmer.stem(other_term)  # cars -> car
                        if other_term not in self.hash_stemmer:
                            self.hash_stemmer[other_term] = ""  # adds stemmed term to hash cache
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
                        if is_doc:
                            if other_term in self.hash_headers and other_term not in self.hash_terms:
                                is_header = 1
                            else:
                                is_header = 0
                            try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                                this_tf = this_term['hash_docs'][self.str_doc_id]['tf_d'] + 1
                                this_header = this_term['hash_docs'][self.str_doc_id]['h']
                                this_term.update({'tf_c': this_term['tf_c'] + 1})
                                this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header + is_header}})
                            except Exception:  # if it's the first occurrence in the new doc -> we update tf_c, df, tf_d
                                this_tf = 1  # new doc therefore new value for tf_d and added to existing tf_c
                                this_term.update({'tf_c': this_term['tf_c'] + this_tf, 'df': this_term['df'] + 1})
                                this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header}})
                                this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                                self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                            if other_term in self.hash_cities:
                                str_new_pos = '(' + str(self.line_in_doc_counter) + ',' + str(self.word_in_line_counter) + ')'
                                try:
                                    str_this_pos = self.hash_cities[other_term][self.str_doc_id]
                                    self.hash_cities[other_term].update({self.str_doc_id: str_this_pos + str_new_pos})
                                except Exception:
                                    self.hash_cities[other_term].update({self.str_doc_id: str_new_pos})
                            if this_tf > self.hash_docs[self.str_doc_id]['max_tf']:  # update max tf
                                self.hash_docs[self.str_doc_id]['max_tf'] = this_tf
                        else:  # if query
                            if other_term not in self.hash_titles[self.str_qry_id] and other_term.lower() not in self.hash_titles[self.str_qry_id]:
                                try:  # if was already seen in curr qry -> we update tf_q
                                    this_tf = this_term[self.str_qry_id] + 1
                                except Exception:  # if it's the first occurrence in the new qry
                                    this_tf = 1  # new qry therefore new value for tf_q
                                this_term.update({self.str_qry_id: this_tf})
                        return  # end of doc/qry update (1+2)
                    else:  # (5) if its a new term (other=PEN and dict='none')
                        if is_doc:
                            if other_term in self.hash_headers and other_term not in self.hash_terms:
                                is_header = 1
                            else:
                                is_header = 0
                            nested_hash = ({'tf_c': 1, 'df': 1, 'hash_docs': {self.str_doc_id: {'tf_d': 1, 'h': is_header}}})
                            self.hash_terms[other_term] = nested_hash
                            this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                            self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                            if other_term in self.hash_cities:
                                str_new_pos = '(' + str(self.line_in_doc_counter) + ',' + str(self.word_in_line_counter) + ')'
                                try:
                                    str_this_pos = self.hash_cities[other_term][self.str_doc_id]
                                    self.hash_cities[other_term].update({self.str_doc_id: str_this_pos + str_new_pos})
                                except Exception:
                                    self.hash_cities[other_term].update({self.str_doc_id: str_new_pos})
                            return  # end of adding a new term
                        else:  # is qry
                            nested_hash = {self.str_qry_id: 1}
                            self.hash_terms[other_term] = nested_hash
                else:  # if the current term is lower case 'pen' (if it's an upper case we don't mind)
                    if other_term in self.hash_terms:  # (3) other=pen and dict=pen -> update
                        this_term = self.hash_terms[other_term]
                        if is_doc:
                            try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                                this_tf = this_term['hash_docs'][self.str_doc_id]['tf_d'] + 1
                                this_header = this_term['hash_docs'][self.str_doc_id]['h']
                                this_term.update({'tf_c': this_term['tf_c'] + 1})
                                if other_term in self.hash_headers and other_term not in self.hash_terms:
                                    is_header = 1
                                else:
                                    is_header = 0
                                this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header + is_header}})
                            except Exception:  # if it's the first occurrence in the new doc -> we update tf_c, df, tf_d
                                this_tf = 1  # new doc therefore new value for tf_d and added to existing tf_c
                                this_term.update({'tf_c': this_term['tf_c'] + this_tf, 'df': this_term['df'] + 1})
                                if other_term in self.hash_headers and other_term not in self.hash_terms:
                                    is_header = 1
                                else:
                                    is_header = 0
                                this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header}})
                                this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                                self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                            if this_tf > self.hash_docs[self.str_doc_id]['max_tf']:  # update max tf
                                self.hash_docs[self.str_doc_id]['max_tf'] = this_tf
                        else:  # if query
                            if other_term not in self.hash_titles[self.str_qry_id] and other_term.lower() not in self.hash_titles[self.str_qry_id]:
                                try:  # if was already seen in curr qry -> we update tf_q
                                    this_tf = this_term[self.str_qry_id] + 1
                                except Exception:  # if it's the first occurrence in the new qry
                                    this_tf = 1  # new qry therefore new value for tf_q
                                this_term.update({self.str_qry_id: this_tf})
                        return  # end of doc/qry update (1+2)
                    else:  # (4) other=pen and Dict=PEN  -> now will be Dict=pen + update
                        temp_term_upper = other_term.upper()  # temp = PEN
                        if temp_term_upper in self.hash_terms:
                            old_term = self.hash_terms[temp_term_upper]  # this_term = PEN
                            this_term = copy.deepcopy(old_term)  # creates new lower case term 'pen'
                            if is_doc:
                                if other_term in self.hash_headers and other_term not in self.hash_terms:
                                    is_header = 1
                                else:
                                    is_header = 0
                                try:  # if was already seen in curr doc -> we update tf_c, tf_d and pos
                                    this_tf = this_term['hash_docs'][self.str_doc_id]['tf_d'] + 1
                                    this_header = this_term['hash_docs'][self.str_doc_id]['h']
                                    this_term.update({'tf_c': this_term['tf_c'] + 1})
                                    this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': this_header + is_header}})
                                except Exception:  # if it's the first occurrence in the new doc -> we update tf_c, df, tf_d
                                    this_tf = 1  # new doc therefore new value for tf_d and added to existing tf_c
                                    this_term.update({'tf_c': this_term['tf_c'] + this_tf, 'df': this_term['df'] + 1})
                                    this_term['hash_docs'].update({self.str_doc_id: {'tf_d': this_tf, 'h': is_header}})
                                    this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                                    self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                                if this_tf > self.hash_docs[self.str_doc_id]['max_tf']:  # update max tf
                                    self.hash_docs[self.str_doc_id]['max_tf'] = this_tf
                            else:  # if query
                                if other_term not in self.hash_titles[self.str_qry_id] and other_term.lower() not in \
                                        self.hash_titles[self.str_qry_id]:
                                    try:  # if was already seen in curr qry -> we update tf_q
                                        this_tf = this_term[self.str_qry_id] + 1
                                    except Exception:  # if it's the first occurrence in the new qry
                                        this_tf = 1  # new qry therefore new value for tf_q
                                    this_term.update({self.str_qry_id: this_tf})
                            self.hash_terms[other_term] = this_term  # adds 'pen'
                            del self.hash_terms[temp_term_upper]  # deletes old upper case term 'PEN'
                            return  # end of doc or qry update (4)
                        else:  # (5) if its a new term (other=pen and dict='none')
                            if is_doc:
                                if other_term in self.hash_headers and other_term not in self.hash_terms:
                                    is_header = 1
                                else:
                                    is_header = 0
                                nested_hash = ({'tf_c': 1, 'df': 1, 'hash_docs': {self.str_doc_id: {'tf_d': 1, 'h': is_header}}})
                                self.hash_terms[other_term] = nested_hash
                                this_unique = self.hash_docs[self.str_doc_id]['unique_count']
                                self.hash_docs[self.str_doc_id]['unique_count'] = this_unique + 1
                            else:  # if query
                                nested_hash = {self.str_qry_id: 1}
                                self.hash_terms[other_term] = nested_hash
                            return
        except Exception:
            print("MotherFucking Term : " + other_term)

    # function implements method upper() #

    def make_upper_case(self, term):
        i = 0
        word = term
        for ch in word:
            if 96 < ord(ch) < 123:
                word = word[:i] + chr(ord(ch) - 32) + word[i + 1:]
            i += 1
        return word

    # function implements method lower() #

    def make_lower_case(self, term):
        i = 0
        word = term
        for ch in word:
            if 64 < ord(ch) < 91:
                word = word[:i] + chr(ord(ch) + 32) + word[i + 1:]
            i += 1
        return word

    # main function filters regular terms of unnecessary punctuations #

    def is_regular_term(self, term, is_doc):
        try:
            if term != '':
                size = len(term) - 1
                last = term[size]
                first = term[0]
                while (term != '' and (size > 0 and last != '') and (last in self.hash_punc or '\"' in last or "\\\\" in last)):
                    term = term[:-1]
                    size -= 1
                    if size > 0:
                        last = term[size]
                while (term != '' and (size > 0 and first != '') and (first in self.hash_punc or '\"' in first or "\\\\" in first)):
                    term = term[1:]
                    size -= 1
                    if size > 0:
                        first = term[0]
                skip = False
                if term != '':
                    for key in self.hash_punc_middle:
                        if key in term:
                            skip = True
                            break
                if not skip and self.clean_term(term, is_doc) and self.valid_range(term):
                    self.term_case_filter(term, is_doc)
        except Exception:
            print("MotherFucking Term : " + term)

    # prevent index increment if double delete
    two_deleted = 0

    # main function receives index of a number token and inserts the token appropriately to the hash terms

    def convert_numbers_in_list(self, index):
        list_t = self.list_tokens
        tmp_term = list_t[index]
        term_size = len(tmp_term)
        while tmp_term[term_size - 1] in self.hash_punc:
            tmp_term = tmp_term[:-1]
            term_size -= 1
        list_t[index] = tmp_term
        # first loop correct number forms
        operation_done = 0
        term = list_t[index]
        dot_pos = term.find('.')
        if dot_pos == len(term) - 1:
            term = term.replace('.', '')
        if '/' not in term and '-' not in term:
            if '$' not in term and 'bn' not in term and 'm' not in term and not self.is_year(index):
                try:
                    float(term)
                    self.list_tokens[index] = self.numbers_rules(term)
                    operation_done = 1
                except ValueError:
                    #print("the argument : | " + self.list_tokens[index] + " | could not be parsed")
                    return 'SyntaxError{}'
            if operation_done == 0 and self.is_year(index):
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

    # function checks if the given term is a number #

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
            except Exception:
                print("index out of bound in: @ is_number")
        ans = all_numbers or contain_special
        return ans

    # function converts number term according to the rules #

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

    # function formats big numbers according to rules #

    def format_num(self, number, sign, mode, after_point):
        zero_killer = 1
        num_desired_format = number[:-mode] + '.' + number[-mode:]
        num_desired_format = list(num_desired_format)
        while num_desired_format[len(num_desired_format) - zero_killer] == '0' and after_point == '':
            num_desired_format[len(num_desired_format) - zero_killer] = ''
            zero_killer = zero_killer + 1
        num_desired_format = "".join(num_desired_format)
        return num_desired_format + after_point + sign

    # function formats dollars according to rules #

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

    # function formats prices according to rules #

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

    # function formats dates according to rules #

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

    # function formats year according to rules #

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

    # function formats asterisks that are replacing '/n' #

    def ignore_asterisk_back_mode(self, index):
        index -= 1
        while index > 0 and self.list_tokens[index] == '*':
            index -= 1
        return index

    # function formats asterisks that are replacing '/n' #

    def ignore_asterisk_front_mode(self, index):
        index += 1
        while index < len(self.list_tokens) - 2 and self.list_tokens[index] == '*':
            index += 1
        return index

    # function formats fractions #

    def is_fraction(self, index):
        to_add = ""
        if index < len(self.list_tokens):
            to_add = self.list_tokens[index - 1] + ' ' + self.list_tokens[index]
            del self.list_tokens[index - 1]
        return to_add

    # function formats percentages #

    def num_percent(self, number):
        return number + "%"

    # function formats numbers #

    def num_dollar(self, number):
        return number + " Dollars"

    # function checks if string represents int #
    def represents_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    # function adds a city line number #

    def city_lines_and_docs(self):
        self.line_counter = self.line_counter + self.str_doc.count('\n')

    # function validates term #

    def valid_range(self, term):
        try:
            ch = ord(term[0])
            return 48 <= ch <= 57 or 65 <= ch <= 90 or 97 <= ch <= 122
        except Exception:
            return False

    # function checks if the term is clean #

    def clean_term(self, term, is_doc):
        try:
            if term != '' and term.lower() not in self.hash_stopwords and term not in self.hash_punc \
                    and term not in self.hash_alphabet:
                if not is_doc:
                    if term.lower() not in self.hash_qry_stopwords:
                        return True
                else:
                    return True
            else:
                if not is_doc:
                    if term.lower() == 'not' or term.lower() == 'non':
                        return True
                return False
        except Exception:
            return

    def analyze_title(self, semantic_model, is_semantic_mode):
        try:
            self.str_txt_title = self.str_txt_title.replace('\n', ' * ')
            list_title = self.str_txt_title.split()
            list_title_token = []
            word_sem = ''
            list_sem = []
            for word in list_title:
                if self.clean_term(word, 0):
                    if "-" in word:
                        try:
                            word_split = word.rstrip().split('-', 1)
                            word1 = word_split[0]
                            if self.clean_term(word1, 0):
                                if self.stemmer:
                                    word1 = self.stemmer.stem(word1)
                                nested_hash = {word1.lower(): ""}
                                try:
                                    self.hash_titles[self.str_qry_id].update(nested_hash)
                                except Exception:
                                    self.hash_titles[self.str_qry_id] = nested_hash
                                if is_semantic_mode:
                                    sem_num = 4
                                else:
                                    sem_num = 1
                                try:
                                    word_sem = self.make_lower_case(word1)
                                    list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                                    new_sem = list_sem[0][0]
                                    if self.stemmer:
                                        new_sem = self.stemmer.stem(new_sem)
                                    list_title_token.append(new_sem)
                                    list_sem = []
                                except Exception:
                                    try:
                                        word_sem = self.make_upper_case(word1)
                                        list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                                        new_sem = list_sem[0][0]
                                        if self.stemmer:
                                            new_sem = self.stemmer.stem(new_sem)
                                        list_title_token.append(new_sem)
                                        list_sem = []
                                    except Exception as e:
                                        a = 0
                            word2 = word_split[1]
                            if self.clean_term(word2, 0):
                                if self.stemmer:
                                    word2 = self.stemmer.stem(word2)
                                nested_hash = {word2.lower(): ""}
                                try:
                                    self.hash_titles[self.str_qry_id].update(nested_hash)
                                except Exception:
                                    self.hash_titles[self.str_qry_id] = nested_hash
                                if is_semantic_mode:
                                    sem_num = 4
                                else:
                                    sem_num = 1
                                try:
                                    word_sem = self.make_lower_case(word2)
                                    list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                                    new_sem = list_sem[0][0]
                                    if self.stemmer:
                                        new_sem = self.stemmer.stem(new_sem)
                                    list_title_token.append(new_sem)
                                    list_sem = []
                                except Exception:
                                    try:
                                        word_sem = self.make_upper_case(word2)
                                        list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                                        new_sem = list_sem[0][0]
                                        if self.stemmer:
                                            new_sem = self.stemmer.stem(new_sem)
                                        list_title_token.append(new_sem)
                                        list_sem = []
                                    except Exception as e:
                                        a = 0
                            if "-" in word2:
                                word_split = word2.rstrip().split('-', 1)
                                word3 = word_split[0]
                                if self.clean_term(word3, 0):
                                    if self.stemmer:
                                        word3 = self.stemmer.stem(word3)
                                    nested_hash = {word3.lower(): ""}
                                    try:
                                        self.hash_titles[self.str_qry_id].update(nested_hash)
                                    except Exception:
                                        self.hash_titles[self.str_qry_id] = nested_hash
                                    if is_semantic_mode:
                                        sem_num = 4
                                    else:
                                        sem_num = 1
                                    try:
                                        word_sem = self.make_lower_case(word3)
                                        list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                                        new_sem = list_sem[0][0]
                                        if self.stemmer:
                                            new_sem = self.stemmer.stem(new_sem)
                                        list_title_token.append(new_sem)
                                        list_sem = []
                                    except Exception:
                                        try:
                                            word_sem = self.make_upper_case(word3)
                                            list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                                            new_sem = list_sem[0][0]
                                            if self.stemmer:
                                                new_sem = self.stemmer.stem(new_sem)
                                            list_title_token.append(new_sem)
                                            list_sem = []
                                        except Exception as e:
                                            a = 0
                                word4 = word_split[1]
                                if self.clean_term(word4, 0):
                                    if self.stemmer:
                                        word4 = self.stemmer.stem(word4)
                                    nested_hash = {word4.lower(): ""}
                                    try:
                                        self.hash_titles[self.str_qry_id].update(nested_hash)
                                    except Exception:
                                        self.hash_titles[self.str_qry_id] = nested_hash
                                    if is_semantic_mode:
                                        sem_num = 4
                                    else:
                                        sem_num = 1
                                    try:
                                        word_sem = self.make_lower_case(word4)
                                        list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                                        new_sem = list_sem[0][0]
                                        if self.stemmer:
                                            new_sem = self.stemmer.stem(new_sem)
                                        list_title_token.append(new_sem)
                                        list_sem = []
                                    except Exception:
                                        try:
                                            word_sem = self.make_upper_case(word4)
                                            list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                                            new_sem = list_sem[0][0]
                                            if self.stemmer:
                                                new_sem = self.stemmer.stem(new_sem)
                                            list_title_token.append(new_sem)
                                            list_sem = []
                                        except Exception as e:
                                            a = 0
                            del word_split
                        except Exception:
                            a = 0
                    if is_semantic_mode:
                        sem_num = 4
                    else:
                        sem_num = 1
                    try:
                        word_sem = self.make_lower_case(word)
                        list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                        new_sem = list_sem[0][0]
                        if self.stemmer:
                            new_sem = self.stemmer.stem(new_sem)
                        list_title_token.append(new_sem)
                    except Exception:
                        try:
                            word_sem = self.make_upper_case(word)
                            list_sem = semantic_model.wv.most_similar(positive=word_sem, topn=1)
                            new_sem = list_sem[0][0]
                            if self.stemmer:
                                new_sem = self.stemmer.stem(new_sem)
                            list_title_token.append(new_sem)
                        except Exception as e:
                            a = 0
                    if self.stemmer:
                        word = self.stemmer.stem(word)
                    nested_hash = {word.lower(): ""}
                    try:
                        self.hash_titles[self.str_qry_id].update(nested_hash)
                    except Exception:
                        self.hash_titles[self.str_qry_id] = nested_hash
            self.list_tokens = list_title
            if len(list_title_token) > 0:
                for token in list_title_token:
                    self.list_tokens.append(token)
        except Exception:
            a = 0

    def analyze_desc(self):
        try:
            self.str_txt_desc = self.str_txt_desc.replace('\n', ' * ')
            if self.stemmer:
                stem_list = self.str_txt_desc.split()
                for stem_word in stem_list:
                    stem_word = self.stemmer.stem(stem_word)
                    self.list_tokens.append(stem_word)
            else:
                self.list_tokens.extend(self.str_txt_desc.split())
        except Exception:
            a = 0

    def analyze_narr(self):
        try:
            self.str_txt_narr = self.str_txt_narr.replace('-', ' ')
            self.str_txt_narr = self.str_txt_narr.split()
            sentence_list = []
            sentence = ''
            for word in self.str_txt_narr:
                last_ch = word[-1:]
                if last_ch == ';' or last_ch == ',':
                    word = word[:-1]
                if self.clean_term(word, 0) and last_ch != '.' and last_ch != ':':
                    sentence = sentence + word + ' '
                elif last_ch == '.' or last_ch == ':' or last_ch == '*' or last_ch == '?':
                    if sentence[-4:] == 'not ' and word == 'relevant:':
                        break
                    word = word[:-1]
                    if self.clean_term(word, 0):
                        sentence = sentence + word
                    if sentence != '' and 'non relevant' not in sentence and 'not relevant' not in sentence:
                        if 'relevant' in sentence:
                            sentence = sentence.replace('relevant', '')
                        sentence_list.append(sentence)
                    sentence = ''
            if self.stemmer:
                stem_list = sentence.split()
                for stem_word in stem_list:
                    stem_word = self.stemmer.stem(stem_word)
                    sentence = sentence + stem_word + ' '
                sentence_list.append(sentence)
            if len(sentence_list) > 0:
                for sentence in sentence_list:
                    self.list_tokens.extend(sentence.split())
        except Exception:
            a = 0

    # main function of the parsing sequence. receives a long string and divides it to tokens #

    def start_parse(self, s_content, is_doc, semantic_model, is_single_qry, is_semantic_mode, is_stemmer_mode):
        if is_doc:
            self.doc_counter += 1
            if s_content:  # sets current document
                self.str_doc = s_content
            try:
                self.str_doc_id = (self.str_doc.split("</DOCNO>", 1)[0]).split("<DOCNO>")[1].strip()
                d_id_split = self.str_doc_id.split('-')
                cut_zeros = int(d_id_split[1])
                d_id = d_id_split[0] + '-' + str(cut_zeros)
                self.str_doc_id = d_id
            except AttributeError:
                a = 0
            try:
                self.str_txt = self.str_doc.split("<TEXT>")[1].strip()
                self.str_txt = self.str_txt.split("</TEXT>")
                self.str_txt = self.str_txt[0]
            except Exception:
                a = 0
            self.str_txt = self.str_txt.replace('*', '')
            self.str_txt = self.str_txt.replace('\n', ' * ')
            self.list_tokens = self.str_txt.split()
            self.hash_docs.update({self.str_doc_id: {'max_tf': 0, 'unique_count': 0,'words':{},'entities':{}}})
            self.set_city()
            self.set_headers()
        else:  # is query
            if is_stemmer_mode:
                self.stemmer = EnglishStemmer()
            if is_single_qry:
                self.str_qry_id = str(randint(100, 999))
                self.str_txt_title = s_content.replace('*', '')
                self.analyze_title(semantic_model, is_semantic_mode)
            else:  # bunch of queries
                try:
                    s_num = s_content.split("<num>")[1]
                    s_num = s_num.split("<title")[0]
                    l_qry_id = s_num.split(":")
                    get_qry_id = l_qry_id[1].split('\n')
                    self.str_qry_id = get_qry_id[0].replace(' ', '')
                    s_title = s_content.split("<title>")[1]
                    s_title = s_title.split("<desc>")[0]
                    self.str_txt_title = s_title.replace('*', '')
                except Exception:
                    a = 0
                try:
                    s_desc = s_content.split("<desc>")[1]
                    s_desc = s_desc.split("<narr>")[0]
                    s_narr = s_content.split("<narr>")[1]
                    s_narr = s_narr.split("</top>")[0]
                    self.str_txt_desc = s_desc.replace('*', '')
                    self.str_txt_narr = s_narr.replace(' - ', '* ')
                except Exception:
                    a = 0
                try:
                    self.analyze_title(semantic_model, is_semantic_mode)
                except Exception:
                    a = 0
                try:
                    self.analyze_desc()
                    self.analyze_narr()
                except Exception:
                    a = 0
        index = 0
        for term in self.list_tokens:
            num_inserted = 0
            if term != '':
                if term == '*':
                    self.line_in_doc_counter += 1
                    self.global_line_counter += 1
                    self.word_in_line_counter = 0
                else:
                    if ',' in term:
                        term = term.replace(',', '')
                        self.list_tokens[index] = term
                    if self.clean_term(term, is_doc):
                        try:
                            if term[0].isdigit() or term[0] == '$':
                                term = self.convert_numbers_in_list(index)
                                if term == 'SyntaxError{}':
                                    term = self.list_tokens[index]
                                    # print('Term| ' +term+' |inserted.')
                                else:
                                    if self.clean_term(term, is_doc):
                                        self.term_case_filter(term, is_doc)
                                    num_inserted = 1
                        except Exception:
                            a = 0
                        if num_inserted == 0:
                            try:
                                if term != '' and term.isalpha() and term.lower() not in self.hash_stopwords:
                                    if term[0].isupper():
                                        if term.lower() not in self.hash_docs[self.str_doc_id]['words']:
                                            if term.upper() in self.hash_docs[self.str_doc_id]['entities']:
                                                self.hash_docs[self.str_doc_id]['entities'][term.upper()] += 1
                                            else:
                                                self.hash_docs[self.str_doc_id]['entities'][term.upper()] = 1
                                        else:
                                            if term.upper() in self.hash_docs[self.str_doc_id]['entities']:
                                                del self.hash_docs[self.str_doc_id]['entities'][term.upper()]
                                                self.hash_docs[self.str_doc_id]['words'][term.lower()] = 0
                                    else:
                                        self.hash_docs[self.str_doc_id]['words'][term.lower()] = 0
                            except Exception as e:
                                a = 0
                            if "--" in term:  # term1--term2
                                try:
                                    list_double = term.split('--')
                                    term1 = list_double[0]
                                    term2 = list_double[1]
                                    if self.clean_term(term1, is_doc):
                                        self.is_regular_term(term1, is_doc)
                                    if self.clean_term(term2, is_doc):
                                        self.is_regular_term(term2, is_doc)
                                    del list_double
                                except Exception:
                                    a = 0
                            elif "-" in term:  # term1-term2-term3
                                try:
                                    word_split = term.rstrip().split('-', 1)
                                    term1 = word_split[0]
                                    if self.clean_term(term1, is_doc):
                                        self.is_regular_term(term1, is_doc)  # term1
                                    term2 = word_split[1]
                                    if self.clean_term(term2, is_doc):
                                        self.is_regular_term(term2, is_doc)  # term2-term3
                                    if "-" in term2:
                                        word_split = term2.rstrip().split('-', 1)
                                        term3 = word_split[0]
                                        if self.clean_term(term3, is_doc):
                                            self.is_regular_term(term3, is_doc)  # term2
                                        term4 = word_split[1]
                                        if self.clean_term(term4, is_doc):
                                            self.is_regular_term(term4, is_doc)  # term3
                                    del word_split
                                except Exception:
                                    a = 0
                            elif "@" in term:  # '@' our new rule
                                list_mail = term.split('@')
                                term1 = list_mail[0]
                                term2 = list_mail[1]
                                if self.clean_term(term1, is_doc):
                                    self.is_regular_term(term1, is_doc)
                                if self.clean_term(term2, is_doc):
                                    self.is_regular_term(term2, is_doc)
                                del list_mail
                            if self.clean_term(term, is_doc):
                                self.is_regular_term(term, is_doc)
                                self.word_in_line_counter += 1
                            index += 1
        if is_doc:
            self.hash_headers = {}
            self.hash_docs[self.str_doc_id]['doc_size'] = index
            del self.hash_docs[self.str_doc_id]['words']



