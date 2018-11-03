import re
import nltk
from Model.TermObject import TermObject


class Parser:

    # initializes strings

    str_doc = ""
    str_txt = ""
    str_doc_id = ""

    # initializes lists & dictionaries (are not case sensitive)

    hash_terms = {}  # hash table representing dictionary of terms

    list_tokens = []

    list_stopwords = []

    list_months = {'january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr',
                   'may', 'june', 'jun', 'july', 'jul', 'august', 'aug', 'september',
                   'sep', 'october', 'oct', 'november', 'nov', 'december', 'dec'}

    list_punc = {'%', ',', '`', ':', ';', '[', ']', '(', ')', '{', "}", '<', '>', '|', '~', '^', '@', '*', '?', '_',
                 '\', '"/"', '"\\"', '"!"', " = ', '#'}

    #  static counter
    """
    def pIF(self):  # pointer to the inverted file
        global count
        self.count += 1
        return self.count
    """
    # constructor #

    def __init__(self, str_doc):
        if str_doc:  # sets current document
            self.str_doc = str_doc

        str_path = 'C:\\Users\\edoli\\Desktop\\SE_PA\\stopwords.txt'  # sets stop word dictionary
        self.get_stopwords(str_path)

        #  self.count = 0  # sets value for hash table

        try:  # gets doc_id
            self.str_doc_id = re.search('<DOCNO>(.+?)</DOCNO>', str_doc).group(1)
        except AttributeError:
            print("marker <DOCNO> not found")

        self.parse_doc()

    # main function for the parser process #

    def parse_doc(self):
        self.extract_text()  # (1) extracts text from doc
        self.tokenize()  # (2) transfers text to list
        #  self.print_list()
        self.term_filter()  # (3) filters list to dictionary

    # function creates stop word list #

    def get_stopwords(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read().replace('\n', ' ')
        self.list_stopwords = data.split()

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
            var = key, "=>", key, ",", value
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
            return True
        else:
            return False

    # function deals with hyphen terms #

    def is_hyphen(self, term):
        self.add_term(term)  # add the whole term "step-by-step"
        while "-" in term:  # add the split terms
            word_split = term.rstrip().split('-', 1)  # step | by-step
            curr_word = word_split[0]
            self.add_term(curr_word)  # adds term "step"
            word_split.remove(curr_word)
            term = word_split[0]
        self.add_term(term)

    # function adds term appropriately #

    def add_term(self, term):
        found = False
        is_upper = False
        other_term = ""
        if term.lower() in self.hash_terms:
            other_term = term.lower()
            is_upper = False
            found = True
        elif term.upper() in self.hash_terms: # if the term exists already
            other_term = term.upper()
            is_upper = True
            found = True
        if found:
            self.term_case_filter(other_term, is_upper)
            term.set_tf()  # updates tf
            if not term.get_doc:  # updates idf
                term.set_idf()
        else:  # if the term is new
            value = TermObject(term, self.str_doc_id)  # Later: remember to remove term from list
            self.hash_terms[term] = value

    # function deals with term case-sensitivity #

    def term_case_filter(self, this_term, is_upper):
        if is_upper and this_term:
            this_term.set_to_lower_case()

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
            self.print_dict()
