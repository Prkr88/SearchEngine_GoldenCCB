import os
import re
from Model.Parser import Parser
import nltk
nltk.download()

def getFiles():
    counter = 0
    for root, dirs, files in os.walk(
            'C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus\\corpus'):
        for file in files:
            ''' print(os.path.join(root, file))'''
            file_path = os.path.join(root, file)
            if counter == 0:
                get_doc_from_file(file_path)
            counter = counter + 1
    print(counter)


def get_doc_from_file(file_path):
    skip_one = 0
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '')
        data_list = data.split("<DOC>")
        for doc in data_list:
            if skip_one == 1:
                doc = "<DOC>" + doc
                p = Parser(doc)

            else:
                skip_one = 1

getFiles()
