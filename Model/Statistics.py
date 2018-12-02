import os
import pickle
from Model.Stemmer import Stemmer
import timeit


class Statistics:
    def __init__(self):
        self.vocabulary = {}
        self.stemmed_vocabulary = {}
        self.cities_hash = {}
        self.corpus_cities = {}
        self.cities_in_docs = {}

    def create_vocabulary(self):
        file_list = self.set_file_list('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\temp_hash_objects')
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key not in self.vocabulary:
                    self.vocabulary[key] = 0
            hash_file.close()
            file_hash_terms = {}
        with open('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\Vocabulary.pkl',
                  'wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)

    def create_corpus_cities(self):
        file_list = self.set_file_list('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\hash_cities_objects')
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key not in self.corpus_cities:
                    self.corpus_cities[key] = 0
            hash_file.close()
            file_hash_terms = {}
        with open('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus_cities.pkl',
                  'wb') as output:
            pickle.dump(self.corpus_cities, output, pickle.HIGHEST_PROTOCOL)

    def load_vocabulary(self):
        path = "C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\Vocabulary.pkl"
        with open(path, 'rb') as vocab:
            vocabulary_to_load = pickle.load(vocab)
        self.vocabulary = vocabulary_to_load

    def load_corpus_cities(self):
        path = "C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus_cities.pkl"
        with open(path, 'rb') as vocab:
            vocabulary_to_load = pickle.load(vocab)
        self.corpus_cities = vocabulary_to_load

    def load_stemmed_vocabulary(self):
        path = "C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\Stemmed_Vocabulary.pkl"
        with open(path, 'rb') as vocab:
            vocabulary_to_load = pickle.load(vocab)
        self.stemmed_vocabulary = vocabulary_to_load

    def load_cities(self):
        path = "C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\cities_data.pkl"
        with open(path, 'rb') as vocab:
            to_load = pickle.load(vocab)
        self.cities_hash = to_load

    def stem_vocabulary(self):
        stemmer = Stemmer()
        for key in self.vocabulary:
            stemmer._stem(key)
        stemmer.save_stemmed_vocabulary()

    def set_file_list(self ,path):
        files_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        # files_list_tmp = []
        # for i in range(20):
        #     files_list_tmp.append(files_list[i])
        return files_list

    def count_numbers(self):
        num_counter = 0
        term_counter = 0
        for key in self.vocabulary:
            term_counter += 1
            try:
                if key[0].isdigit():
                    num_counter += 1
                elif key[1].isdigit():
                    num_counter += 1
            except IndexError:
                pass
        print("number terms: " + str(num_counter))


    def count_cities(self):
        counter = 0
        for key in self.cities_hash:
            upper_key = key.upper()
            if upper_key in self.corpus_cities:
                counter += 1
        print(counter)

    def find_maxtf_city(self):
        file_list = self.set_file_list(
            'C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\temp_hash_objects')
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key in self.corpus_cities:
                    self.cities_in_docs[key] = file_hash_terms[key]
            hash_file.close()
            file_hash_terms = {}
        with open('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\cities_in_docs.pkl',
                  'wb') as output:
            pickle.dump(self.cities_in_docs, output, pickle.HIGHEST_PROTOCOL)

    def load_cities_in_docs(self):
        maxT = 0
        winner =""
        path = "C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\cities_in_docs.pkl"
        with open(path, 'rb') as vocab:
            to_load = pickle.load(vocab)
        self.cities_in_docs = to_load
        for key in self.cities_in_docs:
            if self.cities_in_docs[key]['tf_c'] >= 5:
                for doc_id in self.cities_in_docs[key]['hash_docs']:
                    if self.cities_in_docs[key]['hash_docs'][doc_id]['tf_d'] > maxT:
                        maxT = self.cities_in_docs[key]['hash_docs'][doc_id]['tf_d']
                        winner = doc_id
                print(str(key) +' -> D_ID: ' + str(winner) + 'tf_d: ' + str(maxT))
                maxT = 0
                winner = ""

    def count_countries(self):
        countries = {}
        file_list = self.set_file_list(
            'C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\temp_hash_objects')
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in self.cities_hash:
                if self.cities_hash[key]['Country_Name'] in file_hash_terms or self.cities_hash[key]['Country_Name'].upper() in file_hash_terms:
                    countries[self.cities_hash[key]['Country_Name']] = ""
            hash_file.close()
            file_hash_terms = {}
        print(len(countries))

if __name__ == '__main__':
    stat = Statistics()
    # stat.create_vocabulary()
    #stat.load_vocabulary()
    # stat.stem_vocabulary()
    # stat.load_stemmed_vocabulary()
    #stat.count_numbers()
    #stat.create_corpus_cities()
    stat.load_cities()
    #stat.clean_corpus_cities()
    #stat.load_corpus_cities()
    #stat.find_maxtf_city()
    #stat.load_cities_in_docs()
    #stat.count_countries()
    stat.count_countries()
    print("done")
