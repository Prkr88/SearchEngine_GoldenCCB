import re
import copy
import nltk
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
        path_stopwords = 'C:\\Users\\edoli\\Desktop\\SearchEngine_GoldenCCB\\resources\\stopwords.txt'
        path_keywords = 'C:\\Users\\edoli\\Desktop\\SearchEngine_GoldenCCB\\resources\\keywords.txt'
        self.set_stopwords(path_stopwords)  # sets stop word dictionary
        self.set_keywords(path_keywords)  # sets key word dictionary
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

    '''this function converts all the number in the document acording to the rules'''

    def numbers_rules(self, num_str):
        num_edit = num_str.replace(",", "")
        number_split = num_edit.split(".", 1)
        before_point = number_split[0]
        if len(number_split) > 1:
            after_point = number_split[1]
        else:
            after_point = ''
        if len(before_point) > 9:
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
        print(ans)

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

    def num_precent(self, number):
        return number + "%"

    def num_dollar(self, number):
        return number + " Dollars"

    # function filters all terms #

    def term_filter(self):
        for term in self.list_tokens:
            rule_stopword = self.is_stop_word(term)
            rule_punc = self.is_punc(term)
            if not rule_stopword and not rule_punc:
                self.is_regular_term(term)
        print(self.max_tf)
