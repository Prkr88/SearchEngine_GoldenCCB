from Model.TermData import TermData


class TermObject:

    """
Later: add value parameters: position, bold, etc...
    """

    # static counter for the pointers to the IF

    '''
    def s_count(self):  # pointer to the inverted file
        global count
        self.count += 1
        return self.count
    '''

    pIF_count = 0

    # constructor #

    def __init__(self, term, doc_id, pIF):
        self.hash_term_data = {}
        self.term = term
        self.list_docs = [doc_id]
        self.pIF = pIF
        # self.pIF = self.s_count()
        self.tf = 1
        self.idf = 1
        self.term_data = TermData()
        if doc_id not in self.hash_term_data:
            self.hash_term_data[doc_id] = self.term_data
        if term.isupper():
            self.upper_case = True
        else:
            self.upper_case = False

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, other):
        return other == self.term

    def __ne__(self, other):
        return other != self.term

    def set_tf(self, doc_id):
        if doc_id not in self.hash_term_data:
            self.hash_term_data[doc_id] = TermData()
        term_data = self.hash_term_data[doc_id]
        term_data.update_tf()

    def add_position(self, doc_id, line, offset):
        term_data = self.hash_term_data[doc_id]
        term_data.add_pos_to_list(line, offset)

    def set_idf(self):
        self.idf += 1

    def set_to_lower_case(self):
        self.upper_case = False
        self.term = self.term.lower()

    def set_doc(self, doc_id):
        if not self.list_docs.__contains__(doc_id):
            self.list_docs.append(doc_id)

    def set_pIF(self, pIF):
        self.pIF = pIF

    def get_doc(self, doc_id):
        return self.list_docs.__contains__(doc_id)

    def get_term(self):
        return self.term

    def get_tf(self, doc_id):
        term_data = self.hash_term_data[doc_id]
        return term_data.get_term_tf()

    def get_doc(self, doc_id):
        return doc_id in self.hash_term_data


'''
    def get_tf(self):
        return self.tf

    def get_idf(self):
        return self.idf

    def get_is_uppercase(self):
        return self.upper_case
'''
