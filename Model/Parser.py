import re
import copy
import nltk
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

    list_tokens = []

    list_stopwords = []

    list_keywords = []

    list_punc = {',', '"', '`', ':', ';', '[', ']', '(', ')', '{', "}", '<', '>', '|', '~', '^', '*', '?',
                 '\', ,"``", "\\", """\\""", '"'\\'\\'''", '"!"', "=", "#"}

    max_tf = 0  # static var max_tf for the most frequent term in the document

    # constructor #

    def __init__(self, str_doc):
        if str_doc:  # sets current document
            self.str_doc = str_doc
        project_dir = os.path.dirname(os.path.dirname(__file__))
        str_path_stopwords = 'resources\\stopwords.txt'  # sets stop word dictionary
        str_path_keywords = 'resources\\keywords.txt'  # sets key word dictionary
        abs_stopword_path = os.path.join(project_dir, str_path_stopwords)
        abs_keyword_path = os.path.join(project_dir, str_path_keywords)
        self.set_stopwords(abs_stopword_path)  # sets stop word dictionary
        self.set_keywords(abs_keyword_path)  # sets key word dictionary
        self.set_doc_id(str_doc)  # set the doc's id
        self.set_city_info(str_doc)  # set the city info
        self.parse_doc()  # starts the parsing

        # function sets the document's id #



    def set_doc_id(self, str_doc):
        try:
            self.str_doc_id = re.search('<DOCNO>(.+?)</DOCNO>', str_doc).group(1)
        except AttributeError:
            print("marker <DOCNO> not found")

    # function sets the city's info #

    def set_city_info(self, str_doc):
        try:
            self.str_city_info = re.search('<F P=104>(.+?)</F>', str_doc).group(1)
            info = self.str_city_info.split()
            str_city_name = info[0]
            self.add_city(str_city_name)
        except AttributeError:
            print("marker <F P=104> not found")

    # function adds city #

    def add_city(self, city_name):
        if city_name.upper in self.hash_cities:
            this_city = self.hash_cities[city_name.upper()]
            this_city.set_doc(self.str_doc_id)
        else:
            this_city = CityObject(self.str_doc_id, city_name)
            self.hash_cities[city_name.upper()] = this_city

    # main function for the parser process #

    def parse_doc(self):
        self.extract_text()  # (1) extracts text from doc
        self.tokenize()  # (2) transfers text to list
        #  self.print_list()
        self.term_filter()  # (3) filters list to dictionary

    # function creates stopword list #

    def set_stopwords(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        self.list_stopwords = data.split()

    # function creates keyword list #

    def set_keywords(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        self.list_keywords = data.split()

    # function extracts text from a given document #

    def extract_text(self):
        try:
            self.str_txt = re.search('<TEXT>(.+?)</TEXT>', self.str_doc).group(1)
        except AttributeError:
            print("marker <TEXT> not found")

    # function receives string and returns list #

    def tokenize(self):
        self.list_tokens = nltk.word_tokenize(self.str_txt)
        re.sub("'t", 'ot', "n't, doesn't, can't, don't, a's, ain't")

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
        if self.list_stopwords.__contains__(term):
            self.list_tokens.remove(term)
            return True
        else:
            return False

    # function checking if the term is a key word #

    def is_key_word(self, term):
        if self.list_keywords.__contains__(term):
            self.list_tokens.remove(term)
            return True
        else:
            return False

    # function skips token checking if the term is a punctuation #

    def is_punc(self, term):
        if self.list_punc.__contains__(term):
            self.list_tokens.remove(term)
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

    def count_upper(self, term):
        count = 0
        for ch in term:
            if ch.isupper():
                count += 1
        return count

    # function adds term appropriately #

    def add_term(self, term):

        this_term = self.term_case_filter(term)

        if this_term is not None:  # if the term exists
            this_term.set_tf()  # updates tf
            if this_term.get_tf() > self.max_tf:  # updates max tf for document
                self.max_tf = this_term.get_tf()
            if not this_term.get_doc:  # updates idf
                this_term.set_idf()
        else:                   # if the term is new
            if self.count_upper(term) >= 1:
                term = term.upper()
            else:
                term = term.lower()
            # if term not in self.list_keywords:  # deletes tokens that are not from our keywords
                # self.list_tokens.remove(term)
            value = TermObject(term, self.str_doc_id)  # Later: remember to remove term from list
            self.hash_terms[term] = value

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
        elif found and this_upper and other_upper:
            this_term = self.hash_terms[term.upper()]  # (2) this:First other:First
        elif found:
            this_term = self.hash_terms[term.lower()]  # (3) this:first other:first + (4) this:first other:First

        return this_term

    # function filters regular terms #

    def is_regular_term(self, term):
        if not isinstance(term, int):  # validates that the term is not an integer
            if "-" in term:
                self.is_hyphen(term)
            else:
                self.add_term(term)

    # convert all numbers according to rules

    # prevent index increment if double delete
    two_deleted = 0

    def convert_numbers_in_list(self):
        index = 0
        # first loop correct number forms
        while index < len(self.list_tokens_second_pass):
            if self.has_numbers(self.list_tokens_second_pass[index]):
                if self.is_year(index):
                    self.list_tokens_second_pass[index] = self.numbers_rules(self.list_tokens_second_pass[index])
            index += 1
        # second loop merge according to rules
        index = 0
        while index < len(self.list_tokens_second_pass):
            self.edit_list_by_key_word_prices(index)
            if self.two_deleted == 1:
                self.two_deleted = 0
            else:
                index += 1
            # third loop take care of dates
            index = 0
            while index < len(self.list_tokens_second_pass):
                self.edit_list_by_key_word_dates(index)
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
        num_desired_format = number
        if (float(number)) > 1000:
            num_desired_format = number.replace('.', '')
        return num_desired_format + 'M'

    def edit_list_by_key_word_prices(self, index):
        term_prev = ""
        term_next = ""
        term_next_next = ""
        ans = ""
        need_to_update = 0
        if index > 0:
            term_prev = self.list_tokens_second_pass[index - 1]
        term_current = self.list_tokens_second_pass[index]
        temp_term = list(term_current)
        if index < len(self.list_tokens_second_pass) - 1:
            term_next = self.list_tokens_second_pass[index + 1]
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
            self.list_tokens_second_pass[index] = ans
            del self.list_tokens_second_pass[index + 1]
        if term_next != "" and term_next == 'Thousand' or term_next == 'Million' or term_next == 'Billion' \
                or term_next == 'Trillion' or term_next == 'million' or term_next == 'billion' \
                or term_next == 'trillion' or term_next == 'thousand':
            if index < len(self.list_tokens_second_pass) - 2:
                term_next_next = self.list_tokens_second_pass[index + 2]
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
            self.list_tokens_second_pass[index] = ans
            term_current = ans
            del self.list_tokens_second_pass[index + 1]
            self.two_deleted = 1
            if index < len(self.list_tokens_second_pass) and need_to_update == 1:
                term_next = self.list_tokens_second_pass[index + 1]
        if term_current == 'm' or term_current == 'bn':
            if term_current == 'm':
                ans = self.format_num(term_prev, 'M', 6, '')
                self.list_tokens_second_pass[index] = ans
                del self.list_tokens_second_pass[index - 1]
            if term_current == 'bn':
                ans = self.format_num_dollar_mode(term_prev, 'M')
                term_current = ans
                self.list_tokens_second_pass[index] = ans
                del self.list_tokens_second_pass[index - 1]
                index -= 1
        if term_next != "" and term_next == 'Dollars' or term_next == 'dollars':
            ans = self.num_dollar(term_current)
            self.list_tokens_second_pass[index] = ans
            del self.list_tokens_second_pass[index + 1]
        if term_prev != "" and term_prev == '$':
            ans = self.num_dollar(term_current)
            self.list_tokens_second_pass[index] = ans
            del self.list_tokens_second_pass[index - 1]

    def edit_list_by_key_word_dates(self, index):
        term_prev = ""
        term_next = ""
        ans = ""
        month_num = '0'
        term_current = self.list_tokens_second_pass[index]
        if index > 0:
            term_prev = self.list_tokens_second_pass[index - 1]
        if index < len(self.list_tokens_second_pass) - 1:
            term_next = self.list_tokens_second_pass[index + 1]
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
                self.list_tokens_second_pass[index] = ans
                del self.list_tokens_second_pass[index - 1]
            elif self.represents_int(term_next):
                if len(term_next) == 1:
                    term_next = '0' + term_next
                if len(term_next) > 2:
                    ans = term_next + '-' + month_num
                else:
                    ans = month_num + '-' + term_next
                del self.list_tokens_second_pass[index + 1]
                self.list_tokens_second_pass[index] = ans

    def is_year(self, index):
        term_prev = ""
        term_next = ""
        if index > 0:
            term_prev = self.list_tokens_second_pass[index - 1]
        if index < len(self.list_tokens_second_pass) - 1:
            term_next = self.list_tokens_second_pass[index + 1]
        if term_next in self.list_keywords or term_prev in self.list_keywords:
            return True
        return False

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

    # function filters all terms #

    def term_filter(self):


        for term in self.list_tokens:
            rule_stopword = self.is_stop_word(term)
            rule_punc = self.is_punc(term)
            if not rule_stopword and not rule_punc:
                self.is_regular_term(term)
        print(self.max_tf)
