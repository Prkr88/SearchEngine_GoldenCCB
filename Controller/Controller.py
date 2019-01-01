from Model.ReadFile import ReadFile
from Model.Indexer import Indexer
from Model.Searcher import Searcher
import pickle
import os
import time
import heapq
import shutil
import json
from itertools import chain
import base64


########################################################################################################################
# Class Controller:                                                                                                    #
#                                                                                                                      #
# Listens to actions being made in the GUI by the user and calls the appropriate function in the MODEL                 #
########################################################################################################################


class Controller:
    data_path = ""
    post_path = ""
    stemmer = False
    searcher = None

    def __init__(self, vocab):
        self.vocabulary = vocab
        self.indx = None
        self.total_time = 0
        self.unique_terms = 0
        self.vocabulary_display_mode = ""
        self.capital_cities = {}
        self.doc_entities = {}
        self.hash_docs_data = {}  # {key = docID : value =[maxTf,uniqueCount,docSize,entities] #
        self.doc_counter = 0
        self.city_list_to_limit = []

    def start(self, data_path, post_path, stemmer):
        start = time.time()
        self.data_path = data_path
        self.post_path = post_path
        self.stemmer = stemmer
        if not os.path.exists(self.post_path + '/Engine_Data'):
            os.makedirs(self.post_path + '/Engine_Data')
        if not os.path.exists(self.post_path + '/Engine_Data/temp_hash_objects'):
            os.makedirs(self.post_path + '/Engine_Data/temp_hash_objects')
        if not os.path.exists(self.post_path + '/Engine_Data/Vocabulary'):
            os.makedirs(self.post_path + '/Engine_Data/Vocabulary')
        if not os.path.exists(self.post_path + '/Engine_Data/Cities_hash_objects'):
            os.makedirs(self.post_path + '/Engine_Data/Cities_hash_objects')
        if not os.path.exists(self.post_path + '/Engine_Data/posting_files'):
            os.makedirs(self.post_path + '/Engine_Data/posting_files')
        if not os.path.exists(self.post_path + '/Engine_Data/Docs_hash_objects'):
            os.makedirs(self.post_path + '/Engine_Data/Docs_hash_objects')
        if not os.path.exists(self.post_path + '/Engine_Data/Docs_hash_objects'):
            os.makedirs(self.post_path + '/Engine_Data/Results')
        rf = ReadFile(data_path, post_path, stemmer, self)
        rf.start_evaluating_doc()
        self.update_docs_number()
        self.indx = Indexer(post_path,self.doc_counter)
        self.indx.start_indexing()
        self.create_vocabulary()
        self.unique_terms = len(self.vocabulary)
        #self.create_city_index()
        # self.clear_temp_files()
        # rf.start_evaluating_qry(self.vocabulary)
        end = time.time()
        self.total_time = (end - start)

    def search(self, vocabulary, semantic_model):
        if self.searcher is None:
            # list_user_cities = ['BEIJING', 'TOKYO']
            list_user_cities = None
            self.searcher = Searcher(vocabulary, list_user_cities)
        rf = ReadFile(self.data_path, self.post_path, self.stemmer, self)
        rf.start_evaluating_qry(self.searcher, semantic_model)

    def create_vocabulary(self):
        counter = 0
        byte_offset = 0
        terms_tfc_hash = {}
        term_tfc_list = []
        file_list = self.set_file_list(self.post_path + '\\Engine_Data\\posting_files')
        number_of_files = len(file_list)
        for file in file_list:
            byte_offset = 0
            filename_w_ext = os.path.basename(file)
            filename, file_extension = os.path.splitext(filename_w_ext)
            if filename != 'cities_index':
                with open(file, 'r', encoding='utf-8') as post_file:
                    # seek_list =[33,71,110,14117,24636]
                    # for seek in seek_list:
                    #     post_file.seek(seek)
                    #     line = post_file.readline()
                    #     line = str(line).replace('\n', '')
                    #     print(line)
                    counter += 1
                    if counter % 2 == 0:
                        p_c = float(counter+1)
                        p_c = int(p_c * 100 / number_of_files)
                        self.print_prog(p_c)
                    line = str(post_file.readline())
                    while line:
                        data = line.split('|')[0:2]
                        term = data[0]
                        term_tfc = data[1].split(',')[0]
                        # decoded_offset = base64.b8encode(str(byte_offset).encode('UTF-8'))  # compress as Base32 element
                        self.vocabulary[term] = [filename, byte_offset]
                        # if term.isupper() and term.isalpha():
                        #     self.update_entities(data)
                        byte_offset = byte_offset + self.utf8len(line)  # update Offset
                        terms_tfc_hash[term] = int(term_tfc)  # append to dict for  entities
                        term_tfc_list.append((term, int(term_tfc)))  # append to list for display mode
                        line = str(post_file.readline())
        self.create_hash_docs_data(terms_tfc_hash)
        term_tfc_list = sorted(term_tfc_list, key=lambda tup: tup[1]) # sort list for display
        self.vocabulary['#max_tfc'] = term_tfc_list[len(term_tfc_list)-1][1]
        to_display = "\n".join(
            str(term_tfc_list[i]).replace("'", '') for i in range(len(term_tfc_list)))  # create display file
        # for term_data in term_tfc_list:
        #     self.vocabulary_display_mode += term_data[0] + '->' +term_data[1] + '\n'
        self.vocabulary_display_mode = to_display
        with open(self.post_path + '\\Engine_Data\\Vocabulary\\Vocabulary.pkl', 'wb') as output:
            pickle.dump(self.vocabulary, output, pickle.HIGHEST_PROTOCOL)
        with open(self.post_path + '\\Engine_Data\\Vocabulary\\Vocabulary_display_mode.txt', 'w',
                  encoding='utf-8') as output:
            output.write(self.vocabulary_display_mode)

    def update_docs_number(self):
        file_list = self.set_file_list(self.post_path + '\\Engine_Data\\temp_hash_objects')
        for file in file_list:
            with open(file, 'rb') as hash_file:
                file_hash_terms = pickle.load(hash_file)
                self.doc_counter = self.doc_counter + file_hash_terms['#doc_number']

    def create_city_index(self):
        file_list = self.set_file_list(self.post_path + '/Engine_Data/Cities_hash_objects')
        path = './resources/cities_data.pkl'
        with open(path, 'rb') as data:
            cities_data = pickle.load(data)
        for city_file in file_list:
            with open(city_file, 'rb') as file:
                file_hash_cities = pickle.load(file)
            for key in file_hash_cities:
                if key not in self.capital_cities:
                    if key in cities_data:
                        self.capital_cities[key] = {'Data': '', 'Docs': ''}
                        self.capital_cities[key].update({'Data': cities_data[key], 'Docs': file_hash_cities[key]})
                else:
                    self.capital_cities[key]['Docs'].update(file_hash_cities[key])
        cities_index = ""
        hash_city = self.capital_cities
        tfc = 0
        docs = []
        for key in hash_city:
            city = key
            for doc in hash_city[key]['Docs']:
                docs.append(doc)
                pos = hash_city[key]['Docs'][doc].split(';')
                pos = list(filter(None, pos))
                tfd = len(pos)
                tfc += tfd
            cities_index += city + '|' + str(tfc) + '|' + str(hash_city[key]['Data']) + '|' + ';'.join(docs) + '\n'
            tfc = 0
            docs = []
            cities_data = {}
        with open(self.post_path + "/Engine_Data/posting_files/cities_index.txt", 'w') as file:
            file.write(cities_index)

    def create_hash_docs_data(self,terms_tfc_hash):
        docs_size_in_corpus = 0
        file_list = self.set_file_list(self.post_path + '/Engine_Data/Docs_hash_objects')
        for docs in file_list:
            with open(docs, 'rb') as file:
                hash_docs = pickle.load(file)
            try:
                for doc, data in hash_docs.items():
                    entities = self.update_entities(data['entities'],terms_tfc_hash)
                    self.hash_docs_data[doc] = []
                    self.hash_docs_data[doc].append(data['max_tf'])
                    self.hash_docs_data[doc].append(data['unique_count'])
                    self.hash_docs_data[doc].append(data['doc_size'])
                    self.hash_docs_data[doc].append(entities)
                    docs_size_in_corpus += data['doc_size']
            except Exception as e:
                print(e)
        self.hash_docs_data['#docs_size'] = docs_size_in_corpus
        self.hash_docs_data['#doc_c'] = self.doc_counter
        with open(self.post_path + '/Engine_Data/Vocabulary/hash_docs_data.pkl', 'wb') as output:
            pickle.dump(self.hash_docs_data, output, pickle.HIGHEST_PROTOCOL)

    def set_file_list(self, path):
        files_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        # files_list_tmp = []
        # for i in range(5):
        #     files_list_tmp.append(files_list[i])
        # files_list = files_list_tmp
        return files_list

    def print_prog(self, p_c):
        print('\n' * 100)
        print('Creating Vocabulary:\n[' + '*' * int(p_c / 2) + ' ' * int((100 - p_c) / 2) + str(p_c) + '%' ']')

    def reset_system(self):
        if self.indx != None:
            self.indx.reset_posting_files()
            self.indx = None
            return 1
        else:
            return None

    # Returns the size in bytes of String

    def utf8len(self, s):
        return len(s.encode('utf-8')) + 1

    # entity rank is calculated with term_tfd/term_tfc , in other word - higher rank for strong entities in document in
    # inverse relation to its appearance in the entire corpus
    def update_entities(self,entities, term_tfc_hash):
        term_tfc = 10000
        for entity, tfd in entities.items():
            if entity.upper() in term_tfc_hash:
                term_tfc = term_tfc_hash[entity.upper()]
            elif entity.lower() in term_tfc_hash:
                term_tfc = term_tfc_hash[entity.lower()]
            elif entity in term_tfc_hash:
                term_tfc = term_tfc_hash[entity]
            if term_tfc<3:   # if term tfc is lower than 3 it is probably Garbage
                entities[entity] = 0
            else:
                rank = tfd/term_tfc
                entities[entity] = rank
        sorted_entities = sorted(entities.items(), key=lambda kv: kv[1],reverse=True)
        sorted_cut = []
        for i in range(0, len(sorted_entities)):
            if sorted_entities[i][1] !=0:
                sorted_cut.append(sorted_entities[i])
        sorted_entities = sorted_cut
        sorted_cut = []
        if len(sorted_entities) > 5:
            for i in range(0, 5):
                sorted_cut.append(sorted_entities[i])
            entities = sorted_cut
        else:
            entities = sorted_entities
        return entities




    def clear_temp_files(self):
        shutil.rmtree(self.post_path + '/Engine_Data/Docs_hash_objects')
        shutil.rmtree(self.post_path + '/Engine_Data/Cities_hash_objects')
        shutil.rmtree(self.post_path + '/Engine_Data/temp_hash_objects')


    def set_cities_list_limit(self):
        path = self.post_path.replace('/Engine_Data','')
        with open(path + '/Engine_Data/posting_files/cities_index.txt', 'r', encoding='utf-8') as cities_file:
            line = str(cities_file.readline())
            while line:
                city = line.split('|')
                city = city[0]
                city_tp = (city,0)
                self.city_list_to_limit.append(city_tp)
                line = str(cities_file.readline())
        self.city_list_to_limit = sorted(self.city_list_to_limit, key=lambda tup: tup[0])

    # def update_entities(self, data):
    #     term = data[0]
    #     data_split = data[1].split('<')
    #     term_tfc = data_split[0].split(',')[0]
    #     to_tanslate = (data_split[1])[:-2]
    #     doc_map = self.indx.get_hash_docs(to_tanslate)
    #     for doc_id in doc_map:
    #         rank = int(term_tfc) / doc_map[doc_id][0]
    #         if doc_id not in self.doc_entities:
    #             self.doc_entities[doc_id] = []
    #             heapq.heappush(self.doc_entities[doc_id], (rank, term))
    #         else:
    #             temp_heap = self.doc_entities[doc_id]
    #             if len(temp_heap) < 5:
    #                 heapq.heappush(temp_heap, (rank, term))
    #             else:
    #                 min_val = heapq.heappop(temp_heap)
    #                 if min_val[0] < rank:
    #                     heapq.heappush(temp_heap, (rank, term))
    #                 else:
    #                     heapq.heappush(temp_heap, min_val)
    #                 temp_heap.sort(key=lambda tup: tup[0])
    #                 # self.doc_entities[doc_id] = temp_heap