import os
import re
from Model.Parser import Parser

dictinary_cities = {}


def get_files():
    counter = 0
    for root, dirs, files in os.walk(
            'C:\\Users\\Prkr_Xps\\Documents\\InformationSystems\\Year_C\\SearchEngine\\corpus\\corpus'):
        for file in files:
            ''' print(os.path.join(root, file))'''
            file_path = os.path.join(root, file)
            get_doc_from_file(file_path)
            counter = counter + 1
            print(counter)
    print(counter)
    print(dictinary_cities)
    print(len(dictinary_cities))


def get_doc_from_file(file_path):
    counter = 0
    skip_one = 0
    with open(file_path, 'r') as file:
        data = file.read().replace('\n', '')
        data_list = data.split("<DOC>")
        for doc in data_list:
            if skip_one == 1:
                doc = "<DOC>" + doc
                # p = Parser(doc)
                try:
                    city = ""
                    city = re.search('<F P=104> (.+?) </F>', data).group(1)
                    city = city.split(' ')
                    dictinary_cities[city[1]] = counter
                    counter += 1
                except AttributeError:
                    a = 1
            else:
                skip_one = 1


get_files()
