

class DocObject:

    doc_id = ""
    max_tf = 0
    num_unique_words = 0
    city_origin = ""

    # constructor #

    def __init__(self, doc_id, max_tf, city):
        self.doc_id = doc_id
        self.max_tf = max_tf
        self.city_origin = city

    def set_unique_words(self):
        self.num_unique_words += 1

