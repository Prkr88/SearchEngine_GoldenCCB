import copy
import os
from Model.TermObject import TermObject
from Model.CityObject import CityObject


class Parser:
    # initializes strings

    str_doc = ""
    str_doc_id = ""
    str_city_info = ""
    str_txt = ""

    # initializes lists & dictionaries

    hash_terms = {}  # hash table representing dictionary of terms

    hash_cities = {}

    hash_stopwords = {}

    hash_keywords = {}

    hash_punc = {}

    list_tokens = []

    list_fractions = []

    list_line_seperated = []



    max_tf = 0  # static var max_tf for the most frequent term in the document

    global_line_counter = 0  # global line counter in file
    line_in_doc_counter = 0  # global line counter in doc
    word_in_line_counter = 0  # global line word counter in lines

    # constructor #

    def __init__(self):
        project_dir = os.path.dirname(os.path.dirname(__file__))
        str_path_stopwords = 'resources\\stopwords.txt'  # sets stop word dictionary
        str_path_keywords = 'resources\\keywords.txt'  # sets key word dictionary
        # str_path_test = 'C:\\Users\\edoli\\Desktop\\SE_PA\\test1.txt'
        # self.set_test_file(str_path_test)
        abs_stopword_path = os.path.join(project_dir, str_path_stopwords)
        abs_keyword_path = os.path.join(project_dir, str_path_keywords)
        self.set_stopwords(abs_stopword_path)  # sets stop word dictionary
        self.set_keywords(abs_keyword_path)  # sets key word dictionary
        self.set_puncwords()  # sets punctuation vocabulary

    def start_parse(self, str_doc):
        if str_doc:  # sets current document
            self.str_doc = str_doc
        self.set_doc_id()  # set the doc's id
        # self.set_city_info()  # Later: use city list and use json 1 time
        self.parse_doc()  # starts the parsing

    # function sets the document's id #

    def set_doc_id(self):
        try:
            self.str_doc_id = (self.str_doc.split("</DOCNO>", 1)[0]).split("<DOCNO>")[1].strip()
            print(self.str_doc_id)
        except AttributeError:
            a = 0
            #print("marker <DOCNO> not found")

    # function sets the city's info #

    def set_city_info(self):
        try:
            self.str_city_info = (self.str_doc.split("</F P=104>", 1)[0]).split("<F P=104>")[1].strip()
            str_city_name = self.str_city_info[0]
            self.list_cities.append(str_city_name)
            # self.add_city(str_city_name)
        except AttributeError:
            a = 0
            # print("marker <F P=104> not found")

    # function adds city #

    def add_city(self, city_name):
        if city_name.upper in self.hash_cities:
            this_city = self.hash_cities[city_name.upper()]
            this_city.set_doc(self.str_doc_id)
        else:
            this_city = CityObject(self.str_doc_id, city_name, CityObject.pIF_count)
            self.hash_cities[city_name.upper()] = this_city
            CityObject.pIF_count += 1

    # main function for the parser process #

    def parse_doc(self):
        self.extract_text()  # (1) extracts text from doc
        self.tokenize()  # (2) transfers text to list
        #  self.print_list()
        self.term_filter()  # (3) filters list to dictionary
        del self.str_doc

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

    def set_keywords(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        list_keywords = data.split()
        for word in list_keywords:
            self.hash_keywords[word] = ""
        del list_keywords

    def set_puncwords(self):
        list_punc = {',', '.', '"', '`', ':', ';', '[', ']', '(', ')', '{', "}", '<', '>', '|', '~', '^', '?',
                     '\', ,"``", "``", "\\", """\\""", '"'\\'\\'''", '"!"', "=", "#"}
        for word in list_punc:
            self.hash_punc[word] = ""
        del list_punc

    # function extracts text from a given document #

    def extract_text(self):
        try:
            self.str_txt = self.str_doc.split("<TEXT>")[1].strip()
            self.str_txt = self.str_txt.split("</TEXT>")
            self.str_txt = self.str_txt[0]
        except AttributeError:
            a = 0
            # print("marker <TEXT> not found")

    # function receives string and returns list #

    def tokenize(self):
        # self.str_txt = self.str_txt_test
        self.str_txt = self.str_txt.replace('*', '')
        self.str_txt = self.str_txt.replace('\n', '* ')
        # print(self.str_txt)
        self.list_tokens = self.str_txt.split()
        # self.list_tokens = [t.split('*', 1)[0] for t in self.list_tokens]

    # function prints tokens list #

    def print_list(self):
        print(*self.list_tokens, sep=", ")

    # function prints term dictionary #

    def print_dict(self):
        for key, value in self.hash_terms.items():
            var = "key: ", key, "=>", "value: ", value
            print(var)

    # function skips token checking if the term is a stop word #

    def is_stop_word(self, term):
        if term in self.hash_stopwords:
            # self.list_tokens.remove(term)
            return True
        else:
            return False

    # function checking if the term is a key word #

    def is_key_word(self, term):
        if term in self.hash_keywords:
            # self.list_tokens.remove(term)
            return True
        else:
            return False

    # function skips token checking if the term is a punctuation #

    def is_punc(self, term):  #####FIX THIS####
        if term in self.hash_punc:
            # self.list_tokens.remove(term)
            return True
        else:
            return False

    # function deals with hyphen terms #

    def is_hyphen(self, term):
        self.add_term(term)
        while "-" in term:
            word_split = term.rstrip().split('-', 1)
            curr_word = word_split[0]
            self.add_term(curr_word)
            word_split.remove(curr_word)
            term = word_split[0]
            self.add_term(term)
        del word_split

    def count_upper(self, term):
        count = 0
        for ch in term:
            if ch.isupper():
                count += 1
        return count

    # function adds term appropriately #

    def add_term(self, term):
        this_term = None
        if self.has_numbers(term):
            if term in self.hash_terms:  # if the term exists
                this_term = self.hash_terms[term]
        else:
            this_term = self.term_case_filter(term)
        if this_term is not None:  # if the term exists
            this_term.set_tf(self.str_doc_id)  # updates tf
            if this_term.get_tf(self.str_doc_id) > self.max_tf:  # updates max tf for document
                self.max_tf = this_term.get_tf(self.str_doc_id)
            if not this_term.get_doc:  # updates idf
                this_term.set_idf(self.str_doc_id)
            this_term.add_position(self.str_doc_id, self.line_in_doc_counter, self.word_in_line_counter)
        else:  # if the term is new
            if not self.has_numbers(term):
                if self.count_upper(term) >= 1:
                    term = term.upper()
                else:
                    term = term.lower()
            value = TermObject(term, self.str_doc_id, TermObject.pIF_count)  # Later: remember to remove term from list
            self.hash_terms[term] = value
            TermObject.pIF_count += 1
            value.add_position(self.str_doc_id, self.line_in_doc_counter, self.word_in_line_counter)

    # function deals with term case-sensitivity if the term already exists #

    def term_case_filter(self, term):
        found = False
        this_upper = False
        this_term = None

        if self.count_upper(term) >= 1:
            other_upper = True
        else:
            other_upper = False

        if term.lower() in self.hash_terms:
            this_upper = False
            found = True
        elif term.upper() in self.hash_terms:
            this_upper = True
            found = True

        if found and this_upper and not other_upper:  # (1) this:First other:first -> this:first other:first
            this_term = self.hash_terms[term.upper()]
            this_term.set_to_lower_case()  # sets term to lower case
            new_value = copy.deepcopy(this_term)  # creates new lower case term
            del self.hash_terms[term.upper()]  # deletes old upper case term
            self.hash_terms[term] = new_value
            this_term = self.hash_terms[term.lower()]
            this_term.set_pIF(TermObject.pIF_count)
            TermObject.pIF_count += 1
        elif found and this_upper and other_upper:
            this_term = self.hash_terms[term.upper()]  # (2) this:First other:First
        elif found:
            this_term = self.hash_terms[term.lower()]  # (3) this:first other:first + (4) this:first other:First

        return this_term

    # function cleans terms #

    def clean_punc_term(self, term):
        last_ch = term.strip()[-1]
        first_ch = term.strip()[0]
        if last_ch in self.hash_punc:
            term = term[:-1]
        if first_ch in self.hash_punc:
            term = term[1:]
        if term == '--' or term == "" or term == '-':
            term = ""
        return term

    # function filters regular terms #

    def is_regular_term(self, term):
        # if not self.has_numbers(term):  # validates that the term is not an integer
        term = self.clean_punc_term(term)
        if not term:
            if "-" in term:
                self.is_hyphen(term)
            else:
                if "@" in term:  # '@' our new rule
                    list_mail = term.split('@')
                    self.add_term(list_mail[0])
                    self.add_term(list_mail[1])
                    del list_mail
                self.add_term(term)
        '''else:
            self.list_tokens.append(term)
        if term in self.list_keywords:
            self.list_tokens.append(term)'''

    # convert all numbers according to rules

    # prevent index increment if double delete
    two_deleted = 0

    def convert_numbers_in_list(self):
        index = 0
        # first loop correct number forms
        while index < len(self.list_tokens):
            if self.has_numbers(self.list_tokens[index]) and '/' not in self.list_tokens[index] \
                    and '-' not in self.list_tokens[index]:
                if not self.is_year(index):
                    self.list_tokens[index] = self.numbers_rules(self.list_tokens[index])
            index += 1
        # second loop merge according to rules
        index = 0
        while index < len(self.list_tokens):
            if self.has_numbers(self.list_tokens[index]):
                if '-' not in self.list_tokens[index]:
                    try:
                        self.edit_list_by_key_word_prices(index)
                        if self.two_deleted == 1:
                            self.two_deleted = 0
                            index -= 1
                    except ValueError:
                        print("the argument" + self.list_tokens[index] + " could not be parsed")
            index += 1
        # third loop take care of dates
        index = 0
        while index < len(self.list_tokens):
            self.edit_list_by_key_word_dates(index)
            index += 1
        # fourth loop take care of fractions
        index = 0
        for term in self.list_tokens:
            if '/' in term:
                nums_in_fraction = term.split('/', 1)
                numerator = nums_in_fraction[0]
                denominator = nums_in_fraction[1]
                numerator = self.numbers_rules(numerator)
                denominator = self.numbers_rules(denominator)
                self.list_tokens[index] = numerator + '/' + denominator
                if index > 0 and '/' not in self.list_tokens[index - 1]:
                    if self.has_numbers(self.list_tokens[index - 1]):
                        to_add = self.is_fraction(index)
                        self.list_tokens[index] = to_add
            index += 1

    def has_numbers(self, term):
        return any(char.isdigit() for char in term)

    # convert number term according to rules

    def numbers_rules(self, num_str):
        num_edit = num_str.replace(",", "")
        number_split = num_edit.split(".", 1)
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
        return num_desired_format + 'M'

    def edit_list_by_key_word_prices(self, index):
        term_prev = ""
        term_next = ""
        term_next_next = ""
        ans = ""
        need_to_update = 0
        index_front = 0
        index_back = 0
        if index > 0:
            index_back = self.ignore_asterisk_back_mode(index)
            term_prev = self.list_tokens[index_back]
        term_current = self.list_tokens[index]
        temp_term = list(term_current)
        if index < len(self.list_tokens) - 1:
            index_front = self.ignore_asterisk_front_mode(index)
            term_next = self.list_tokens[index_front]
        if 'm' in temp_term:
            temp_term[temp_term.index('m')] = 'M'
            term_current = "".join(temp_term)
        if term_current.find('b') != -1:
            b_index = temp_term.index('b')
            float_num = float(term_current[:b_index]) * 1000
            if float_num.is_integer():
                float_num = int(float_num)
            temp_term = str(float_num)
            term_current = temp_term + 'M'
        if term_next != "" and term_next == '%' or term_next == 'percent' or term_next == 'percentage':
            ans = self.num_percent(term_current)
            self.list_tokens[index] = ans
            del self.list_tokens[index + 1]
        if term_next != "" and term_next == 'Thousand' or term_next == 'Million' or term_next == 'Billion' \
                or term_next == 'Trillion' or term_next == 'million' or term_next == 'billion' \
                or term_next == 'trillion' or term_next == 'thousand':
            if index < len(self.list_tokens) - 2:
                term_next_next = self.list_tokens[index + 2]
            if term_prev != "" and term_prev == '$':
                if term_next == 'Thousand' or term_next == 'thousand':
                    ans = self.format_num_dollar_mode(str(float(term_current) / 1000))
                if term_next == 'Million' or term_next == 'million':
                    ans = self.format_num_dollar_mode(term_current)
                if term_next == 'Billion' or term_next == 'billion':
                    ans = self.format_num_dollar_mode(term_current + '000')
                if term_next == 'Trillion' or term_next == 'trillion':
                    ans = self.format_num_dollar_mode(term_current + '000000')
            elif term_next_next != "" and term_next_next == 'Dollars' or term_next_next == 'dollars':
                if term_next == 'Thousand' or term_next == 'thousand':
                    ans = self.format_num_dollar_mode(str(float(term_current) / 1000))
                if term_next == 'Million' or term_next == 'million':
                    ans = self.format_num_dollar_mode(term_current)
                if term_next == 'Billion' or term_next == 'billion':
                    ans = self.format_num_dollar_mode(term_current + '000')
                if term_next == 'Trillion' or term_next == 'trillion':
                    ans = self.format_num_dollar_mode(term_current + '000000')
                need_to_update = 1
            else:
                if term_next == 'Thousand' or term_next == 'thousand':
                    ans = self.format_num(term_current, 'K', 3, '')
                if term_next == 'Million' or term_next == 'million':
                    ans = self.format_num(term_current, 'M', 6, '')
                if term_next == 'Billion' or term_next == 'Trillion' or term_next == 'billion' or term_next == 'trillion':
                    ans = self.format_num(term_current, 'B', 9, '')
            self.list_tokens[index] = ans
            term_current = ans
            del self.list_tokens[index_front]
            self.two_deleted = 1
            if index < len(self.list_tokens) and need_to_update == 1:
                term_next = self.list_tokens[index_front]
        if term_current == 'm' or term_current == 'bn':
            if term_current == 'm':
                ans = self.format_num(term_prev, 'M', 6, '')
                self.list_tokens[index] = ans
                del self.list_tokens[index_back]
            if term_current == 'bn':
                ans = self.format_num_dollar_mode(term_prev, 'M')
                term_current = ans
                self.list_tokens[index] = ans
                del self.list_tokens[index_back]
                index -= 1
        if term_next != "" and term_next == 'Dollars' or term_next == 'dollars':
            ans = self.num_dollar(term_current)
            self.list_tokens[index] = ans
            del self.list_tokens[index_front]
        if term_prev != "" and term_prev == '$':
            ans = self.num_dollar(term_current)
            self.list_tokens[index] = ans
            del self.list_tokens[index_back]

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
        if term_next in self.hash_keywords or term_prev in self.hash_keywords:
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

    def term_filter(self):
        # self.convert_numbers_in_list()
        index = 0
        for term in self.list_tokens:
            if term == '*':
                self.line_in_doc_counter += 1
                self.global_line_counter += 1
                self.word_in_line_counter = 0
            else:
                rule_stopword = self.is_stop_word(term)
                rule_punc = self.is_punc(term)
                if not rule_stopword and not rule_punc:
                    if self.has_numbers(term):
                        self.convert_numbers_in_list(index)
                    else:
                        self.is_regular_term(term)
                        self.word_in_line_counter += 1
            index += 1
        print(self.max_tf)

        '''  self.convert_numbers_in_list()
                   for term in self.list_tokens_second_pass:
                       if '-' in term:
                           self.is_hyphen_number_mode(term)
                       else:
                           self.add_term_number_mode(term)'''
