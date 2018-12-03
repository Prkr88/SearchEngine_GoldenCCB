import os
import pickle
from Model.Stemmer import Stemmer
import timeit
import numpy as np
import matplotlib.pyplot as plt
from scipy import special


class Statistics:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path + '/Statistics'):
            os.makedirs(path + '/Statistics')
        self.vocabulary = {}
        self.vocabulary_tfc = {}
        self.stemmed_vocabulary = {}
        self.cities_hash = {}
        self.corpus_cities = {}
        self.cities_in_docs = {}
        self.file_list = self.set_file_list(self.path + '/temp_hash_objects')

    def create_vocabulary(self):
        file_list = self.file_list
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key not in self.vocabulary:
                    self.vocabulary[key] = 0
            hash_file.close()
            file_hash_terms = {}
        with open(self.path + '/Vocabulary/Vocabulary.pkl', 'wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)

    def create_vocabulary_tfc(self):
        file_list = self.file_list
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key not in self.vocabulary_tfc:
                    self.vocabulary_tfc[key] = file_hash_terms[key]['tf_c']
                else:
                    self.vocabulary_tfc[key] = self.vocabulary_tfc[key] + file_hash_terms[key]['tf_c']
            hash_file.close()
            file_hash_terms = {}
        with open(self.path + '/Vocabulary/Vocabulary_tfc.pkl', 'wb') as output:
            pickle.dump(self.vocabulary_tfc, output, pickle.HIGHEST_PROTOCOL)

    def create_corpus_cities(self):
        file_list = self.set_file_list(self.path + '/Cities_hash_objects')
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key not in self.corpus_cities:
                    self.corpus_cities[key] = 0
            hash_file.close()
            file_hash_terms = {}
        with open(self.path + '/Statistics/corpus_cities.pkl', 'wb') as output:
            pickle.dump(self.corpus_cities, output, pickle.HIGHEST_PROTOCOL)

    def load_pickle_file(self, path):
        with open(path, 'rb') as file:
            _to_load = pickle.load(file)
        return _to_load

    # def load_vocabulary(self):
    #     path = self.path + '/Vocabulary/Vocabulary.pkl'
    #     with open(path, 'rb') as vocab:
    #         vocabulary_to_load = pickle.load(vocab)
    #     self.vocabulary = vocabulary_to_load

    # def load_corpus_cities(self):
    #     path =self.path +'/Statistics/corpus_cities.pkl'
    #     with open(path, 'rb') as vocab:
    #         vocabulary_to_load = pickle.load(vocab)
    #     self.corpus_cities = vocabulary_to_load

    # def load_stemmed_vocabulary(self):
    #     path = self.path +'/Statistics/Stemmed_Vocabulary.pkl'
    #     with open(path, 'rb') as vocab:
    #         vocabulary_to_load = pickle.load(vocab)
    #     self.stemmed_vocabulary = vocabulary_to_load

    # def load_cities(self):
    #     path = "../resources/cities_data.pkl"
    #     with open(path, 'rb') as vocab:
    #         to_load = pickle.load(vocab)
    #     self.cities_hash = to_load

    # def load_vocabulary_tfc(self):
    #     path = "C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\vocabulary_tfc.pkl"
    #     with open(path, 'rb') as vocab:
    #         vocabulary_to_load = pickle.load(vocab)
    #     self.vocabulary_tfc = vocabulary_to_load

    def stem_vocabulary(self):
        stemmer = Stemmer()
        for key in self.vocabulary:
            stemmer._stem(key)
        stemmer.save_stemmed_vocabulary(self.path)

    def set_file_list(self, path):
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
        print("Number terms: " + str(num_counter))

    def count_cities(self):
        counter = 0
        for key in self.cities_hash:
            upper_key = key.upper()
            if upper_key in self.corpus_cities:
                counter += 1
        print(counter)

    def create_cities_with_tfc(self):
        file_list = self.file_list
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key in self.corpus_cities:
                    self.cities_in_docs[key] = file_hash_terms[key]
            hash_file.close()
            file_hash_terms = {}
        with open(self.path + '/Statistics/cities_in_docs.pkl', 'wb') as output:
            pickle.dump(self.cities_in_docs, output, pickle.HIGHEST_PROTOCOL)

    def print_cities_max_tf(self):
        maxT = 0
        winner_doc = ""
        path = self.path + '/Statistics/cities_in_docs.pkl'
        with open(path, 'rb') as vocab:
            to_load = pickle.load(vocab)
        self.cities_in_docs = to_load
        for key in self.cities_in_docs:
            if self.cities_in_docs[key]['tf_c'] >= 10:
                for doc_id in self.cities_in_docs[key]['hash_docs']:
                    if self.cities_in_docs[key]['hash_docs'][doc_id]['tf_d'] > maxT:
                        maxT = self.cities_in_docs[key]['hash_docs'][doc_id]['tf_d']
                        winner_doc = doc_id
                print(str(key) +' -> D_ID: ' + str(winner_doc) + ', tf_d: ' + str(maxT))
                maxT = 0
                winner = ""

    def count_countries(self):
        countries = {}
        file_list = self.file_list
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in self.cities_hash:
                if self.cities_hash[key]['Country_Name'] in file_hash_terms or self.cities_hash[key][
                    'Country_Name'].upper() in file_hash_terms:
                    countries[self.cities_hash[key]['Country_Name']] = ""
            hash_file.close()
            file_hash_terms = {}
        print("Number of Countries :" + str(len(countries)))

    def terms_to_file_sorted_by_most_common_to_file(self):
        self.vocabulary_tfc = stat.load_pickle_file(stat.path + '/Vocabulary/vocabulary_tfc.pkl')
        sorted_vocab_tfc = sorted(self.vocabulary_tfc.items(), key=lambda x: x[1])
        with open(self.path + '/Statistics/sorted_vocab_tfc.txt', 'w') as f:
            for item in sorted_vocab_tfc:
                f.write(str(item) + '\n')

    def plot_zipf_law(self):
        ranks = len(self.vocabulary_tfc)
        # convert value of frequency to numpy array
        frequency = {key:value for key, value in self.vocabulary_tfc.items()[0:100]}
        s = frequency.values()
        s = np.array(s)
        # Calculate zipf and plot the data
        a = 2.  # distribution parameter
        count, bins, ignored = plt.hist(s[s < ranks], ranks, normed=True)
        x = np.arange(1., 50.)
        y = x ** (-a) / special.zetac(a)
        plt.plot(x, y / max(y), linewidth=2, color='r')
        plt.show()

if __name__ == '__main__':
    path = 'C:/Users/Prkr_Xps/Documents/InformationSystems/Year_C/SearchEngine/Engine_Data'
    stat = Statistics(path)
    # stat.create_vocabulary()
    # print("Vocabulary Created")
    # stat.create_vocabulary_tfc()
    # print("Vocabulary_tfc Created")
    # stat.stem_vocabulary()
    # print("Stemmed_Vocabulary Created")
    # stat.create_corpus_cities()
    # print("Cities Corpus file Created")
    # stat.create_cities_with_tfc()
    # print("Cities in docs file Created")
    stat.vocabulary = stat.load_pickle_file(stat.path + '/Vocabulary/Vocabulary.pkl')
    stat.stemmed_vocabulary = stat.load_pickle_file(stat.path + '/Vocabulary/Stemmed_Vocabulary.pkl')
    stat.vocabulary_tfc = stat.load_pickle_file(stat.path + '/Vocabulary/Vocabulary_tfc.pkl')
    stat.cities_hash = stat.load_pickle_file("../resources/cities_data.pkl")
    stat.corpus_cities = stat.load_pickle_file(stat.path + '/Statistics/corpus_cities.pkl')
    stat.cities_in_docs = stat.load_pickle_file(stat.path + '/Statistics/cities_in_docs.pkl')
    #stat.print_cities_max_tf()
    # stat.count_countries()
    # stat.count_numbers()
    # stat.terms_to_file_sorted_by_most_common_to_file()
    stat.plot_zipf_law()
    print("done")
