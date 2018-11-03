class TermObject:

    """
Later: add value parameters: position, bold, etc...
    """

    # static counter for the pointers to the IF

    def s_count(self):  # pointer to the inverted file
        global count
        self.count += 1
        return self.count

    count = 0

    # constructor #

    def __init__(self, term, doc_id):
        self.term = term
        self.list_docs = [doc_id]
        self.pIF = self.s_count()
        self.tf = 1
        self.idf = 1
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

    def set_tf(self):
        self.tf += 1

    def set_idf(self):
        self.idf += 1

    def set_to_lower_case(self):
        self.upper_case = False
        self.term = self.term.lower()

    def get_doc(self, doc_id):
        self.list_docs.__contains__(doc_id)

    def get_term(self):
        return self.term

    def get_tf(self):
        return self.tf

    def get_idf(self):
        return self.idf

    def get_is_uppercase(self):
        return self.upper_case
