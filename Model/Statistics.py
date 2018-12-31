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
        self.vocabulary_with_pointers ={}
        self.file_list = self.set_file_list(self.path + '/temp_hash_objects')
        self.stat_log = open(path + '/Statistics/statistics_log.txt', 'w')

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
        with open(self.path + '/Statistics/Vocabulary.pkl', 'wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)

    def create_vocabulary_tfc(self):
        file_list = self.file_list
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            del file_hash_terms['#doc_number']
            for key in file_hash_terms:
                if key not in self.vocabulary_tfc:
                    self.vocabulary_tfc[key] = file_hash_terms[key]['tf_c']
                else:
                    self.vocabulary_tfc[key] = self.vocabulary_tfc[key] + file_hash_terms[key]['tf_c']
            hash_file.close()
            file_hash_terms = {}
        with open(self.path + '/Statistics/Vocabulary_tfc.pkl', 'wb') as output:
            pickle.dump(self.vocabulary_tfc, output, pickle.HIGHEST_PROTOCOL)

    def create_corpus_cities(self):
        with open('../resources/cities_of_the_world.pkl', 'rb') as file:
            cities_of_the_world = pickle.load(file)
        file_list = self.set_file_list(self.path + '/Cities_hash_objects')
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
            for key in file_hash_terms:
                if key in cities_of_the_world and key not in self.corpus_cities:
                    self.corpus_cities[key] = 0
            hash_file.close()
            file_hash_terms = {}
        with open(self.path + '/Statistics/corpus_cities.pkl', 'wb') as output:
            pickle.dump(self.corpus_cities, output, pickle.HIGHEST_PROTOCOL)
        print(len(self.corpus_cities))

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
        return num_counter

    def count_capital_cities(self):
        counter = 0
        for key in self.cities_hash:
            upper_key = key.upper()
            if upper_key in self.corpus_cities:
                counter += 1
        return counter

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
        ans =""
        maxT = 0
        winner_doc = ""
        tresh_hold = 15
        path = self.path + '/Statistics/cities_in_docs.pkl'
        with open(path, 'rb') as vocab:
            to_load = pickle.load(vocab)
        self.cities_in_docs = to_load
        for key in self.cities_in_docs:
            if self.cities_in_docs[key]['tf_c'] >= 15:
                for doc_id in self.cities_in_docs[key]['hash_docs']:
                    if self.cities_in_docs[key]['hash_docs'][doc_id]['tf_d'] > maxT:
                        maxT = self.cities_in_docs[key]['hash_docs'][doc_id]['tf_d']
                        winner_doc = doc_id
                if maxT>tresh_hold:
                    ans = ans + str(key) + ' -> D_ID: ' + str(winner_doc) + ', tf_d: ' + str(maxT) + '\n'
                maxT = 0
                winner = ""
        return ans

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
        return str(len(countries))

    def terms_to_file_sorted_by_most_common_to_file(self):
        ans = "least common Terms: \n"
        common = 0
        counter = 0
        self.vocabulary_tfc = stat.load_pickle_file(stat.path + '/Statistics/vocabulary_tfc.pkl')
        sorted_vocab_tfc = sorted(self.vocabulary_tfc.items(), key=lambda x: x[1])
        with open(self.path + '/Statistics/sorted_vocab_tfc.txt', 'w') as f:
            for item in sorted_vocab_tfc:
                if counter<10:
                    ans = ans +(str(item)) +'\n'
                if counter == 10:
                    ans = ans + "\nMost common Terms: \n"
                if counter>len(sorted_vocab_tfc)-30:
                    ans = ans + (str(item)) +'\n'
                counter += 1
                f.write(str(item) + '\n')
        return ans

    def plot_zipf_law(self):
        ranks = len(self.vocabulary_tfc)
        values = []
        # convert value of frequency to numpy array
        # frequency = {key: value for key, value in self.vocabulary_tfc.items()[0:1000]}
        frequencies = self.vocabulary_tfc
        for key in frequencies:
            values.append(frequencies[key])
        s = values
        s = np.array(s)
        # Calculate zipf and plot the data
        a = 2.  # distribution parameter
        count, bins, ignored = plt.hist(s[s < 20], 20, normed=True)
        x = np.arange(1., 50.)
        #y = x ** (-a) / special.zetac(a)
        y = x ** (-a) / special.zetac(a)
        plt.plot(x, y / max(y), linewidth=2, color='r')
        #plt.show()
        plt.savefig(stat.path + '/Statistics/zipf_law_Graph.png')

    def write_statistics_log(self):
        self.stat_log.write('#Number of Unique Terms: ' + str(len(stat.vocabulary)) + '\n\n')
        self.stat_log.write('#Number of terms who are numbers: ' + str(stat.count_numbers()) + '\n\n')
        self.stat_log.write('#Number of countries in corpus: ' + str(stat.count_countries()) + '\n\n')
        self.stat_log.write('#Number of cities in corpus: ' + str(len(self.corpus_cities)) + '\n\n')
        self.stat_log.write('#Number of non capital cities in corpus: ' +
                            str(len(self.corpus_cities) - self.count_capital_cities()) + '\n\n')
        self.stat_log.write(self.terms_to_file_sorted_by_most_common_to_file() + '\n\n')
        self.stat_log.write("Most common cities: " + self.print_cities_max_tf() + '\n\n')

    def write_pointers_to_file(self):
        with open(self.path + '/Statistics/vocab_pointers.txt', 'w') as f:
            for item in self.vocabulary_with_pointers:
                f.write(str(item) + ' -->' + str(self.vocabulary_with_pointers[item]) + '\n')

    def write_some_pickles(self):
        counter = 0
        file_list = self.set_file_list(self.path + '/temp_hash_objects')
        for path in file_list:
            hash_file = self.load_pickle_file(path)
            with open(self.path + '/Statistics/KAKA_PICKLE/'+str(counter) +'.txt', 'a') as f:
                for item in hash_file:
                    f.write(str(item) + ' -->' + str(hash_file[item]) + '\n')
            counter += 1

if __name__ == '__main__':
    path = 'C:/Users/Prkr_Xps/Documents/InformationSystems/Year_C/SearchEngine/Engine_Data'
    stat = Statistics(path)
    # stat.create_vocabulary()
    # print("Vocabulary Created")
    # stat.create_vocabulary_tfc()
    # print("Vocabulary_tfc Created")
    # stat.stem_vocabulary()
    # print("Stemmed_Vocabulary Created")
    #stat.create_corpus_cities()
    # print("Cities Corpus file Created")
    # stat.create_cities_with_tfc()
    # print("Cities in docs file Created")
    stat.vocabulary = stat.load_pickle_file(stat.path + '/Statistics/Vocabulary.pkl')
    stat.stemmed_vocabulary = stat.load_pickle_file(stat.path + '/Statistics/Stemmed_Vocabulary.pkl')
    stat.vocabulary_tfc = stat.load_pickle_file(stat.path + '/Statistics/Vocabulary_tfc.pkl')
    stat.cities_hash = stat.load_pickle_file("../resources/cities_data.pkl")
    stat.corpus_cities = stat.load_pickle_file(stat.path + '/Statistics/corpus_cities.pkl')
    stat.cities_in_docs = stat.load_pickle_file(stat.path + '/Statistics/cities_in_docs.pkl')
    stat.vocabulary_with_pointers = stat.load_pickle_file(stat.path + '/Vocabulary/Vocabulary_with_pointers.pkl')
    stat.terms_to_file_sorted_by_most_common_to_file()
    # stat.write_statistics_log()
    # stat.plot_zipf_law()
    #stat.vocabulary_with_pointers = stat.load_pickle_file(stat.path + '/Vocabulary/Vocabulary_with_pointers.pkl')
    #stat.write_pointers_to_file()
    #stat.write_some_pickles()
    #print(str(len(stat.corpus_cities) - stat.count_capital_cities()))
    #print("stemmed " + str(len(stat.stemmed_vocabulary)))
    print("done")
