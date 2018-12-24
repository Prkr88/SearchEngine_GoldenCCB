from Model.Ranker import Ranker
LOWERCASE = 0
UPPERCASE = 1
LOWERBOUND = 0
UPPERBOUND = 1


class Searcher:

    hash_qry_terms = {}
    hash_qry = {}
    hash_index_terms = {}
    hash_results = {}
    list_file_index = []
    vocabulary = {}
        
    def __init__(self, hash_qry_terms, max_tf, b, vocabulary):
        self.vocabulary = vocabulary
        self.hash_qry_terms = hash_qry_terms
        self.set_hash_qry()
        self.set_hash_index_terms()
        self.run(max_tf, b)

    def set_hash_qry(self):
        for term, qry_val in self.hash_qry_terms.items():
            for qry_id, tf_q in qry_val.items():
                # term_seek = self.vocabulary[term][1]
                term_seek = 0
                try:
                    self.hash_qry[qry_id].update({term: [tf_q, term_seek]})
                except Exception:
                    self.hash_qry.update({qry_id: {term: [tf_q, term_seek]}})

    def set_hash_index_terms(self):
        path_source = 'C:/Users/edoli/Desktop/SE_PA/Engine_Data/posting_files/'
        path_target = '.txt'
        condition_list = [[[48, 57], [48, 57]], [[65, 66], [97, 98]], [[67, 68], [99, 100]], [[69, 70], [101, 102]],
                          [[71, 72], [103, 104]], [[73, 75], [105, 107]], [[76, 78], [108, 110]],
                          [[79, 81], [111, 113]], [[82, 83], [114, 115]], [[84, 86], [116, 118]],
                          [[87, 90], [119, 122]]]
        file_list = ['num', 'ab', 'cd', 'ef', 'gh', 'ijk', 'lmn', 'opq', 'rs', 'tuv', 'wxyz']
        size = len(file_list)
        hash_seeker = {}  # key: file_name, value: list_terms
        for qry_id, qry_val in self.hash_qry.items():  # loops query by query
            for q_term, l_data in qry_val.items():  # loops query term by query term
                file_key = 0
                if q_term and len(q_term) > 0:
                    file_key = ord(q_term[0])
                for posting_index in range(0, size):
                    if condition_list[posting_index][LOWERCASE][LOWERBOUND] <= file_key <= condition_list[posting_index][LOWERCASE][UPPERBOUND] or condition_list[posting_index][UPPERCASE][LOWERBOUND] <= file_key <= condition_list[posting_index][UPPERCASE][UPPERBOUND]:
                        file_name = file_list[posting_index]
                        term_seek = l_data[1]
                        try:
                            hash_seeker[file_name].append([q_term, term_seek])
                        except Exception:
                            hash_seeker[file_name] = [[q_term, term_seek]]
            for curr_file_name, list_data in hash_seeker.items():  # loops file by file to seek from
                if list_data is not None:
                    curr_file_name = path_source + curr_file_name + path_target
                    with open(curr_file_name, 'r', encoding='utf-8') as post_file:
                        for term_ptr in list_data:  # seek_list =[33,71,110,14117,24636]
                            row = term_ptr[1]
                            post_file.seek(row)
                            line = post_file.readline()
                            term_data = str(line).replace('\n', '')
                            l_info = term_data.split('|')
                            term = l_info[0]
                            data = l_info[1]
                            self.hash_index_terms[term] = data

    def run(self, max_tf, b):
        r = Ranker(max_tf, b)
        r.start_rank(self.hash_qry, self.hash_index_terms)







