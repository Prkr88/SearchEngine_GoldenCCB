

class CityObject:

    # constructor #

    def __init__(self, doc_id, city_name):
        self.list_docs = [doc_id]
        self.city_name = city_name
        self.state_name = ""
        self.state_population = ""
        self.state_currency = ""

    def __hash__(self):
        return hash(self.city_name)

    def __eq__(self, other):
        return other == self.city_name

    def __ne__(self, other):
        return other != self.city_name

    def get_doc(self, doc_id):
        doc = self.list_docs.__contains__(doc_id)
        return doc

    def get_city_name(self):
        return self.city_name

    def get_state_name(self):
        return self.state_name

    def set_doc(self, doc_id):
        if not self.list_docs.__contains__(doc_id):
            self.list_docs.append(doc_id)

    def set_state_name(self, other):
        self.state_name = other

    def set_state_population(self, other):
        self.state_population = other

    def set_state_currency(self, other):
        self.state_currency = other

