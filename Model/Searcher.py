import pickle
import time

from Model.Ranker import Ranker
LOWERCASE = 0
UPPERCASE = 1
LOWERBOUND = 0
UPPERBOUND = 1


class Searcher:

    vocabulary = {}
    hash_doc_data = {}
    hash_qry_parser = {}
    hash_qry = {}
    hash_seeker = {}
    hash_posting = {}
    hash_docs = {}
    hash_cities_limit = {}
    tuple_results = []
    list_user_cities = []
    M = 0
    k = 0
    avgdl = 0
    ranker = None

    def __init__(self, vocabulary, list_user_cities):
        self.list_user_cities = list_user_cities
        self.vocabulary = vocabulary
        self.k = self.vocabulary['#max_tfc']
        self.set_hash_doc_data()
        self.set_cities_limit()
        self.ranker = Ranker(self.k, self.avgdl, self.M, self.hash_doc_data)
        path = 'C:/Users/edoli/Desktop/SE_PA/Engine_Data/results.txt'
        with open(path, 'w', encoding='utf-8') as file:
            file.close()

    def set_cities_limit(self):
        path = 'C:/Users/edoli/Desktop/SE_PA/Engine_Data/posting_files/cities_index.txt'
        with open(path, 'r', encoding='utf-8') as file:
            list_cities = [line.strip() for line in file]
            file.close()
        for curr_city_list in list_cities:
            nested_docs = {}
            data_list = curr_city_list.split('|')
            city_name = data_list[0]
            doc_string = data_list[3]
            doc_list = doc_string.split(';')
            while len(doc_list) > 0:
                curr_doc_id = doc_list[0]
                nested_docs[curr_doc_id] = ''
                del doc_list[0]
            self.hash_cities_limit[city_name] = nested_docs

    def search(self, hash_qry_parser, hash_titles):
        start = time.time()
        self.ranker.set_hash_titles(hash_titles)
        self.hash_qry_parser = hash_qry_parser
        self.set_hash_qry()
        self.set_hash_seeker()
        end = time.time()
        print('Total search time: ' + str(end - start))

    def set_hash_doc_data(self):
        hash_path = 'C:/Users/edoli/Desktop/SE_PA/Engine_Data/Vocabulary/hash_docs_data.pkl'
        with open(hash_path, 'rb') as input_object:
            self.hash_doc_data = pickle.load(input_object)
        try:
            self.M = self.hash_doc_data['#doc_c']
        except Exception:
            self.M = 475000
        docs_total_size = self.hash_doc_data['#docs_size']
        self.avgdl = float("{0:.4f}".format(docs_total_size / self.M))

    def set_hash_qry(self):
        for term, qry_val in self.hash_qry_parser.items():
            for qry_id, tf_q in qry_val.items():
                resume = True
                try:
                    seek_term = self.vocabulary[term][1]
                except Exception:
                    try:
                        if 64 < ord(term[0]) < 91:
                            seek_term = self.vocabulary[term.lower()][1]
                        else:
                            if 96 < ord(term[0]) < 123:
                                seek_term = self.vocabulary[term.upper()][1]
                    except Exception:
                        resume = False  # if the term is not stored in the indexing database we neglect it
                if resume:
                    try:
                        self.hash_qry[qry_id].update({term: [tf_q, seek_term]})
                    except Exception:
                        self.hash_qry.update({qry_id: {term: [tf_q, seek_term]}})

    def set_hash_seeker(self):
        condition_list = [[[48, 57], [48, 57]], [[65, 66], [97, 98]], [[67, 68], [99, 100]], [[69, 70], [101, 102]],
                          [[71, 72], [103, 104]], [[73, 75], [105, 107]], [[76, 78], [108, 110]],
                          [[79, 81], [111, 113]], [[82, 83], [114, 115]], [[84, 86], [116, 118]],
                          [[87, 90], [119, 122]]]
        file_list = ['num', 'ab', 'cd', 'ef', 'gh', 'ijk', 'lmn', 'opq', 'rs', 'tuv', 'wxyz']
        size = len(file_list)
        for qry_id, qry_val in self.hash_qry.items():  # loops query by query
            self.hash_seeker = {}
            self.hash_docs = {}
            self.hash_posting = {}
            qry_max_tf = 1
            for q_term, l_data in qry_val.items():  # loops query term by query term
                file_key = 0
                if q_term and len(q_term) > 0:
                    file_key = ord(q_term[0])
                for posting_index in range(0, size):
                    if condition_list[posting_index][LOWERCASE][LOWERBOUND] <= file_key <= condition_list[posting_index][LOWERCASE][UPPERBOUND] or condition_list[posting_index][UPPERCASE][LOWERBOUND] <= file_key <= condition_list[posting_index][UPPERCASE][UPPERBOUND]:
                        file_name = file_list[posting_index]
                        tf_q = l_data[0]
                        seek_term = l_data[1]
                        if tf_q > qry_max_tf:
                            qry_max_tf = tf_q
                        try:
                            self.hash_seeker[file_name].append([q_term, seek_term, tf_q])
                        except Exception:
                            self.hash_seeker[file_name] = [[q_term, seek_term, tf_q]]
            self.set_hash_posting()
            self.set_hash_docs()
            self.tuple_results = self.ranker.start_rank_bm25(self.hash_docs, qry_max_tf, qry_id)
            print('QueryID: ' + qry_id + ' Relevant Docs: ' + '\n' + str(qry_val) + '\n')
            i = 1
            for tup_res in self.tuple_results:
                print('Rank #' + str(i) + ' = ' + tup_res[0] + ' Score: ' + str(tup_res[1]))
                i += 1
            print('\n')
            self.write_to_trec_eval(qry_id, qry_val)

    def write_to_trec_eval(self, qry_id, qry_val):
        iter = str(0)
        i = 1
        path = 'C:/Users/edoli/Desktop/SE_PA/Engine_Data/results.txt'
        with open(path, 'a', encoding='utf-8') as file:
            for tup_res in self.tuple_results:
                doc_id = tup_res[0]
                rank = str(tup_res[1])
                sim = str(float(42.38))
                run_id = str(i)
                str_to_write = qry_id + ' ' + iter + ' ' + doc_id + ' ' + rank + ' ' + sim + ' ' + run_id + '\n'
                file.write(str_to_write)
                i += 1

    def set_hash_posting(self):
        path_source = 'C:/Users/edoli/Desktop/SE_PA/Engine_Data/posting_files/'
        path_target = '.txt'
        for curr_file_name, list_data in self.hash_seeker.items():  # loops file by file to seek from
            if list_data is not None:
                curr_file_name = path_source + curr_file_name + path_target
                with open(curr_file_name, 'r', encoding='utf-8') as post_file:
                    for nested_list in list_data:  # seek_list =[33,71,110,14117,24636]
                        row = nested_list[1]
                        tf_q = str(nested_list[2]) + ","
                        try:
                            post_file.seek(row)
                            line = post_file.readline()
                            term_data = str(line).replace('\n', '')
                            l_info = term_data.split('|')
                            term = l_info[0]
                            data = tf_q + l_info[1]
                            self.hash_posting[term] = data
                        except Exception:
                            print("Row: " + row + " not found")

    def validate_doc(self, other_doc_id):
        for city in self.list_user_cities:
            if other_doc_id in self.hash_cities_limit[city]:
                return True
        return False

    def set_hash_docs(self):
        for term, value in self.hash_posting.items():
            try:
                resume = True
                value_term = value.split('>')
                list_gbl = value_term[0].split('<')
                other_global = list_gbl[0].split("'")[0].split(',')
                other_tf_q = int(other_global[0])
                other_float_idf = float(other_global[3])
                list_lcl = list_gbl[1].split(':')
                other_doc_id = list_lcl[0]
                other_lcl = list_lcl[1].split(':')[0].split(',')
                other_tf_d = int(other_lcl[0])
                other_header = int(other_lcl[1])
                if self.list_user_cities is not None:
                    resume = self.validate_doc(other_doc_id)
                if resume:
                    try:
                        self.hash_docs[other_doc_id].update({term: [other_tf_q, other_tf_d, other_float_idf, other_header]})
                    except Exception:
                        self.hash_docs[other_doc_id] = {term: [other_tf_q, other_tf_d, other_float_idf, other_header]}
                prev_doc_id = other_doc_id.split('-')[0]
                prev_gap_id = int(other_doc_id.split('-')[1])
                del value_term[0], list_gbl, list_lcl
                while len(value_term) > 1:  # starts from 2nd iteration
                    info_list = value_term[0].split(':')
                    curr_full_doc_id = info_list[0]
                    if curr_full_doc_id[0].isdigit():  # same doc id
                        curr_doc_id = int(curr_full_doc_id)
                        curr_id = curr_doc_id + prev_gap_id
                        other_doc_id = str(prev_doc_id) + '-' + str(curr_id)
                        info_list = info_list[1].split(':')
                        info_list = info_list[0].split(',')
                        other_tf_d = int(info_list[0])
                        other_header = int(info_list[1])
                        if self.list_user_cities is not None:
                            resume = self.validate_doc(other_doc_id)
                        if resume:
                            try:
                                self.hash_docs[other_doc_id].update(
                                    {term: [other_tf_q, other_tf_d, other_float_idf, other_header]})
                            except Exception:
                                self.hash_docs[other_doc_id] = {
                                    term: [other_tf_q, other_tf_d, other_float_idf, other_header]}
                        prev_gap_id = curr_id
                    else:
                        other_doc_id = curr_full_doc_id  # new doc id
                        info_list = info_list[1].split(',')
                        other_tf_d = int(info_list[0])
                        other_header = int(info_list[1])
                        if self.list_user_cities is not None:
                            resume = self.validate_doc(other_doc_id)
                        if resume:
                            try:
                                self.hash_docs[other_doc_id].update(
                                    {term: [other_tf_q, other_tf_d, other_float_idf, other_header]})
                            except Exception:
                                self.hash_docs[other_doc_id] = {
                                    term: [other_tf_q, other_tf_d, other_float_idf, other_header]}
                        last_info = curr_full_doc_id.split('-')
                        prev_doc_id = last_info[0]
                        prev_gap_id = int(last_info[1])
                    del value_term[0]
            except Exception:
                # print("term: " + other_term + "id: " + other_doc_id + " " + "DecompressorException")
                a = 0
