import re
import nltk
from Model.TermObject import TermObject


class Parser:

    str_doc = ""
    str_txt = ""
    str_doc_id = ""

    list_tokens = []

    # initializes dictionaries (are not case sensitive)

    dict_terms = {}

    dict_stopWords = {'a', 'is', 'the', 'for', 'in', 'on'}

    dict_months = {'january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr',
                   'may', 'june', 'jun', 'july', 'jul', 'august', 'aug', 'september',
                   'sep', 'october', 'oct', 'november', 'nov', 'december', 'dec'}

    dict_punc = {'%', ',', '`', ':', ';', '[', ']', '(', ')', '{', "}", '<', '>', '|', '~', '^', '@', '*', '?', '_',
                 '\', '"/"', '"\\"', '"!"', " = ', '#'}

    # constructor #

    def __init__(self, str_doc):
        if str_doc:
            self.str_doc = str_doc
            try:
                self.str_doc_id = re.search('<DOCNO>(.+?)</DOCNO>', str_doc).group(1)
            except AttributeError:
                print("marker <DOCNO> not found")
        self.parse_doc()

    # main function for the parser process #

    def parse_doc(self):
        self.extract_text()  # (1) extracts text from doc
        self.tokenize()  # (2) transfers text to list
        self.print_list()
        self.term_filter()  # (3) filters list to dictionary

    # function extracts text from a given document #

    def extract_text(self):
        try:
            self.str_txt = re.search('<TEXT>(.+?)</TEXT>', self.str_doc).group(1)
        except AttributeError:
            print("marker <TEXT> not found")

    # function receives string and returns list #

    def tokenize(self):
        self.list_tokens = nltk.word_tokenize(self.str_txt)
        re.sub("'t", 'ot', "n't, doesn't, can't, don't")

    # function prints tokens list #

    def print_list(self):
        print(*self.list_tokens, sep=", ")

    # function prints term dictionary #

    def print_dict(self):
        for key, tf, idf in self.dict_terms.items():
            var = key, "=>", tf, ",", idf
            print(var)

    # function skips token checking if the term is a stop word #

    def is_stop_word(self, term):
        if self.dict_stopWords.__contains__(term):
            self.list_tokens.remove(term)
            return True
        else:
            return False

    # function skips token checking if the term is a punctuation #

    def is_punc(self, term):
        if self.dict_punc.__contains__(term):
            self.list_tokens.remove(term)
            return True
        else:
            return False

    # function deals with hyphen terms #

    def is_hyphen(self, term):
        if self.dict_terms.__contains__('-'):  # if term contains hyphen
            TermObject(term, self.str_doc_id)  # add the whole term "step-by-step"
            word_split = []
            while term.__contains__("-"):  # add the split terms
                word_split = term.split("-")  # step | by-step
                curr_word = word_split[0]
                word_split.remove(curr_word)
                TermObject(curr_word, self.str_doc_id)  # adds term "step"
            last_word = word_split[0]
            TermObject(last_word, self.str_doc_id)

    # function adds term from list to dictionary #

    def add_new_term(self, term):
        TermObject(term, self.str_doc_id)  # Later: remember to remove term from list

    # function adds existing term appropriately #

    def add_existing_term(self, term):
        curr_term = self.dict_terms.get(term)
        self.term_case_filter(curr_term)
        curr_term.set_tf()  # updates tf
        if not curr_term.get_doc:  # updates idf
            curr_term.set_idf()

    # function deals with term case-sensitivity #

    def term_case_filter(self, term):
        curr_term = self.dict_terms.get(term)
        dict_uppercase = curr_term.get_is_uppercase()  # checks case differences and changes appropriately
        this_uppercase = term.isupper()
        if dict_uppercase and not this_uppercase:
            curr_term.set_to_lower_case()

    # function filters regular terms #

    def is_regular_term(self, term):
        if not isinstance(term, int):  # if the term is not an integer
            if not self.dict_terms.__contains__(term):  # entering block to add term to dictionary if doesn't exist yet
                if self.dict_terms.__contains__('-'):
                    self.is_hyphen(term)
                else:
                    self.add_new_term(term)
            else:  # if term does exist, we add to the dictionary and update the terms parameters
                    self.add_existing_term(term)

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
