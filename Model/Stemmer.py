from nltk.stem.snowball import EnglishStemmer
import pickle

class Stemmer:

    def __init__(self):
        self.stemmer = EnglishStemmer()
        self.s_corp = {}  # stemms for corpus
        # self.s_doc = {}  # stemms for a doc (hash cache)

    def _stem(self, term):
        if term in self.s_corp:  # (1) existing 'car'
            this_count = self.s_corp[term]
            self.s_corp.update({term: this_count + 1})
            return term
        else:
            stemmed_term = self.stemmer.stem(term)
            try:  # (2) 'cars' and stem 'car' exists
                this_count = self.s_corp[stemmed_term]
                self.s_corp.update({stemmed_term: this_count + 1})
            except KeyError:  # (3) new 'car' or new 'cars'
                self.s_corp[stemmed_term] = 1
            return stemmed_term

    def save_stemmed_vocabulary(self):
        with open('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\Stemmed_Vocabulary.pkl', 'wb') as output:
            pickle.dump(self.s_corp, output, pickle.HIGHEST_PROTOCOL)

