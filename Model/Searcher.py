from Model.Ranker import Ranker
LOWERCASE = 0
UPPERCASE = 1
LOWERBOUND = 0
UPPERBOUND = 1


class Searcher:

    hash_qry_parser = {}
    hash_qry = {}
    hash_seeker = {}  # key: file_name, value_term: list_terms
    hash_posting = {}
    hash_docs = {}
    tuple_results = []
    vocabulary = {}

    def __init__(self, hash_qry_parser, max_tf, b, vocabulary):
        self.max_tf = max_tf
        self.b = b
        self.vocabulary = vocabulary
        self.hash_qry_parser = hash_qry_parser
        self.set_hash_qry()
        self.set_hash_seeker()

    def set_hash_qry(self):
        for term, qry_val in self.hash_qry_parser.items():
            for qry_id, tf_q in qry_val.items():
                # term_seek = self.vocabulary[term][1]
                term_seek = 0
                try:
                    self.hash_qry[qry_id].update({term: [tf_q, term_seek]})
                except Exception:
                    self.hash_qry.update({qry_id: {term: [tf_q, term_seek]}})

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
            for q_term, l_data in qry_val.items():  # loops query term by query term
                file_key = 0
                if q_term and len(q_term) > 0:
                    file_key = ord(q_term[0])
                for posting_index in range(0, size):
                    if condition_list[posting_index][LOWERCASE][LOWERBOUND] <= file_key <= condition_list[posting_index][LOWERCASE][UPPERBOUND] or condition_list[posting_index][UPPERCASE][LOWERBOUND] <= file_key <= condition_list[posting_index][UPPERCASE][UPPERBOUND]:
                        file_name = file_list[posting_index]
                        tf_q = l_data[0]
                        term_seek = l_data[1]
                        try:
                            self.hash_seeker[file_name].append([q_term, term_seek, tf_q])
                        except Exception:
                            self.hash_seeker[file_name] = [[q_term, term_seek, tf_q]]
                        self.hash_seeker[file_name].append([q_term, term_seek, tf_q])
            self.set_hash_posting()
            self.set_hash_docs()
            self.run(self.max_tf, self.b)

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
                        post_file.seek(row)
                        line = post_file.readline()
                        term_data = str(line).replace('\n', '')
                        l_info = term_data.split('|')
                        term = l_info[0]
                        data = l_info[1]
                        data = tf_q + '28,' + data
                        self.hash_posting[term] = data

    def set_hash_docs(self):
        for term, value in self.hash_posting.items():
            other_doc_id = ''
            hash_temp_doc = {}
            try:
                value_term = value.split('>')
                list_gbl = value_term[0].split('<')
                other_global = list_gbl[0].split("'")[0].split(',')
                other_tf_q = int(other_global[0])
                other_idf = int(other_global[3])
                list_lcl = list_gbl[1].split(':')
                other_doc_id = list_lcl[0]
                other_lcl = list_lcl[1].split(':')[0].split(',')
                other_tf_d = int(other_lcl[0])
                other_header = int(other_lcl[1])
                try:
                    self.hash_docs[other_doc_id].update({term: [other_tf_q, other_tf_d, other_idf, other_header]})
                except Exception:
                    self.hash_docs[other_doc_id] = {term: [other_tf_q, other_tf_d, other_idf, other_header]}
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
                        try:
                            self.hash_docs[other_doc_id].update({term: [other_tf_q, other_tf_d, other_idf, other_header]})
                        except Exception:
                            self.hash_docs[other_doc_id] = {term: [other_tf_q, other_tf_d, other_idf, other_header]}
                        prev_gap_id = curr_id
                    else:
                        other_doc_id = curr_full_doc_id  # new doc id
                        info_list = info_list[1].split(',')
                        other_tf_d = int(info_list[0])
                        other_header = int(info_list[1])
                        try:
                            self.hash_docs[other_doc_id].update({term: [other_tf_q, other_tf_d, other_idf, other_header]})
                        except Exception:
                            self.hash_docs[other_doc_id] = {term: [other_tf_q, other_tf_d, other_idf, other_header]}
                        last_info = curr_full_doc_id.split('-')
                        prev_doc_id = last_info[0]
                        prev_gap_id = int(last_info[1])
                    del value_term[0]
            except Exception:
                a = 0
                # print("term: " + other_term + "id: " + other_doc_id + " " + "DecompressorException")

    def run(self, max_tf, b):
        r = Ranker(max_tf, b)
        doc_size = 100
        doc_avg = 50
        self.tuple_results = r.start_rank(self.hash_docs, doc_size, doc_avg)







