class TermObject:

    """
Later: add value parameters: position, bold, etc...
    """

    term = ""
    tf = 0
    idf = 0
    upper_case = False
    list_docs = []

    def __init__(self, term, doc_id):
        self.term = term
        self.list_docs.append(doc_id)
        if term.isupper():
            self.upper_case = True

    def set_tf(self):
        self.tf += 1

    def set_idf(self):
        self.idf += 1

    def set_to_lower_case(self):
        self.upper_case = False

    def get_doc(self, doc_id):
        self.list_docs.__contains__(doc_id)

    def get_tf(self):
        return self.tf

    def get_idf(self):
        return self.idf

    def get_is_uppercase(self):
        return self.upper_case
