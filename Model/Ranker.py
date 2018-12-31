from numpy import sqrt


class Ranker:

    hash_doc_data = {}
    hash_titles = {}

    def __init__(self, k, avgdl, M, hash_doc_data):
        self.k = k
        # self.k = 2
        self.avgdl = avgdl
        self.N = M
        self.b = 0.7
        self.h_const = 30
        self.hash_doc_data = hash_doc_data

    def set_hash_titles(self, hash_titles):
        self.hash_titles = hash_titles

    def set_title_hit(self, hash_terms, hash_curr_qry_titles):
        title_hit = 1
        length = len(hash_curr_qry_titles)
        bool_hits = [False] * length
        i = 0
        for term, value in hash_terms.items():
            if term.lower() in hash_curr_qry_titles:
                bool_hits[i] = True
                i += 1
        for bool_value in bool_hits:
            if bool_value:
                title_hit += 100
            else:
                title_hit *= 0.0005
        return title_hit

    def start_rank_bm25(self, hash_docs, qry_max_tf, qry_id):
        tuple_results = []
        hash_curr_qry_titles = self.hash_titles[qry_id]
        for doc_id, hash_terms in hash_docs.items():
            if doc_id == 'FBIS4-66185' or doc_id == 'LA111389-74':
                bingo = True
            title_hit = self.set_title_hit(hash_terms, hash_curr_qry_titles)
            bm25 = 0
            try:
                doc_size = self.hash_doc_data[doc_id][2]
            except Exception:
                doc_size = self.avgdl
            for term, value in hash_terms.items():
                if term.lower() in hash_curr_qry_titles:
                    term_hit = 5
                else:
                    term_hit = 1
                tf_q = value[0] / qry_max_tf
                try:
                    max_tf_d = self.hash_doc_data[doc_id][0]
                except Exception:
                    max_tf_d = 1
                # tf_d = value[1] / max_tf_d
                tf_d = value[1]
                idf = value[2]
                h = value[3]
                nmr = (self.k + 1) * tf_d + (self.h_const * h)
                dnmr = tf_d + self.k * (1 - self.b + (self.b * (doc_size / self.avgdl)))
                fraction = nmr / dnmr
                value = (tf_q * term_hit) * fraction * idf
                bm25 += value
            # tuple_results = tuple_results + (doc_id, bm25)
            if bm25 > 0:
                bm25 = float("{0:.5f}".format(bm25 * title_hit))
                tuple_results.append((doc_id, bm25))
        # tuple_results = sorted(tuple_results, key=lambda tup: tup[1])
        tuple_results = sorted(tuple_results, key=lambda tup: (-tup[1], tup[0]))
        if len(tuple_results) > 50:
            tuple_results = tuple_results[0:50]
        return tuple_results

    def start_rank_cossim(self, hash_docs):
        for doc_id, hash_terms in hash_docs.items():
            cossim = 0
            for term, value in hash_terms.items():
                tf_q = value[0]
                tf_d = value[1]
                idf = value[2]
                h = value[3]
                w_value = tf_d * idf * tf_q
                # sqrt_value = sqrt(pow(w, 2))
