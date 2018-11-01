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

    # function filters regular terms #

    def is_regular_term(self, term):
        if not isinstance(term, int):  # if the term is not an integer
            if not self.dict_terms.__contains__(term):  # adds term to dictionary if doesn't exist yet
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
                else:
                    TermObject(term, self.str_doc_id)
            else:  # if it does exist, we add to the dictionary and update the terms parameters
                curr_term = self.dict_terms.get(term)
                dict_uppercase = curr_term.get_is_uppercase()  # checks case differences and changes appropriately
                this_uppercase = term.isupper()
                if dict_uppercase and not this_uppercase:
                    curr_term.set_to_lower_case()
                curr_term.set_tf()  # updates tf
                if not curr_term.get_doc:  # updates idf
                    curr_term.set_idf()

    # function filters all terms #

    def term_filter(self):
        for term in self.list_tokens:
            self.is_stop_word(term)
            self.is_regular_term(term)
