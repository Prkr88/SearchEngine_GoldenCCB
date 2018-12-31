import gensim
import os
import pickle
import re


class DocLiner(object):
    def __init__(self, corpus_path, engine_data_path):
        self.corpus_path = corpus_path
        self.engine_data_path = engine_data_path
        self.train_data_path = engine_data_path + '//Semantics'
        self.counter = 0
        self.vocabulary = self.load_vocabulary()
        self.list_terminate = [',', '.', '\n', ':']
        self.list_garbage = ['INTRODUCTION', 'SUMMARY', 'LANGUAGE', 'language', 'CELLRULE', 'TABLECELL', 'ROWRULE',
                             'TABLEROW', 'summary' ,'english' ,'by','french', 'portuguese',]
        if not os.path.exists(self.engine_data_path + '/Semantics'):
            os.makedirs(self.engine_data_path + '/Semantics')

    def __iter__(self):
        for line in open(self.train_data_path + '//docs_to_train.txt'):
            self.counter +=1
            if self.counter%1000 == 0:
                print(self.counter)
            # for line in open(self.train_data_path + '//mini_train.txt'):
            yield line.split()

    def load_vocabulary(self):
        path = self.engine_data_path + '/Vocabulary/Vocabulary.pkl'
        with open(path, 'rb') as vocab:
            vocabulary_to_load = pickle.load(vocab)
        return vocabulary_to_load

    def create_sentences(self):
        file_list = self.set_file_list()
        skip_one = 0
        counter = 0
        words_in_doc = []
        for file_name in file_list:
            with open(file_name, 'r') as file:
                data = file.read()
                data_list = data.split("<DOC>")
                del data
                for doc in data_list:
                    if skip_one == 0:
                        skip_one = 1
                    else:
                        try:
                            text = doc.split("<TEXT>")[1].strip()
                            text = text.split("</TEXT>")
                            text = text[0]
                            for term in self.list_terminate:
                                text = text.replace(term, '')
                            text = re.sub(' +', ' ', text)
                            if text[0] == ' ':
                                text[0] = ''
                            text = text.split(' ')
                            for word in text:
                                if word.lower() in self.vocabulary and not word.isnumeric() and word.lower() not in self.list_garbage:
                                    words_in_doc.append(word.lower())
                                if word.upper() in self.vocabulary and not word.isnumeric() and word.lower() not in self.list_garbage:
                                    words_in_doc.append(word.upper())
                            if len(words_in_doc) > 0:
                                words_in_doc.append('\n')
                        except Exception:
                            a=0
                line_to_file = ' '.join(words_in_doc)
                line_to_file = line_to_file.replace('\n ', '\n')
                with open(self.engine_data_path + '/Semantics/docs_to_train.txt', 'a') as output:
                    output.write(line_to_file)
                    words_in_doc = []
                    counter +=1
                    if counter%55 == 0:
                        print(counter)

    def set_file_list(self):
        files_list = []
        for root, dirs, files in os.walk(self.corpus_path):
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)
        # files_list_tmp = []
        # for i in range(100):
        #     files_list_tmp.append(files_list[i])
        # files_list = files_list_tmp
        return files_list

    def print_sentences(self):
        counter = 0
        for s in train_data:
            if counter > 10:
                break
            with open(self.engine_data_path + '/Semantics/mini_train.txt', 'a') as output:
                output.write(' '.join(s) + '\n')
                counter += 1


train_data = DocLiner('C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus\\corpus',
                      'C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\Engine_Data')  # a memory-friendly iterator
# train_data.create_sentences()
# train_data.print_sentences()
model = gensim.models.Word2Vec(train_data, workers=8)
# model.save(train_data.train_data_path + '/word2vec.model')
model = gensim.models.Word2Vec.load(train_data.train_data_path + '/word2vec.model')
w1 = 'dog'
try:
    most_similar = model.wv.most_similar(positive=w1, topn=6)
    print(most_similar)
except KeyError:
    print('sorry , this word does not exsist in dictionary')

# with open(train_data.engine_data_path +'/Vocabulary/hash_docs_data.pkl', 'rb') as input:
#     hash_data = pickle.load(input)
# print(hash_data)

