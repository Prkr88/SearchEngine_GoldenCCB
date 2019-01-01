from numpy import sqrt


class Ranker:

    hash_doc_data = {}
    hash_titles = {}
    hash_view = {}
    hash_results = {}

    def __init__(self, k, avgdl, M, hash_doc_data):
        # self.k = k
        self.k = 2
        self.avgdl = avgdl
        self.N = M
        self.b = 0.6
        self.l = 0.2
        self.h_const = 30
        self.w_bm25 = 0.25
        self.w_cossim = 0.75
        self.hash_doc_data = hash_doc_data

    def set_hash_titles(self, hash_titles):
        self.hash_titles = hash_titles

    def start_rank(self, hash_docs, qry_max_tf, qry_id):
        self.start_rank_bm25(hash_docs, qry_id)
        self.start_rank_cossim(hash_docs, qry_max_tf, qry_id)
        return self.start_filter_results()

    def start_rank_bm25(self, hash_docs, qry_id):
        hash_curr_qry_titles = self.hash_titles[qry_id]
        for doc_id, hash_terms in hash_docs.items():
            # if doc_id == 'FBIS4-66185' or doc_id == 'LA111389-74':
            #     bingo = True
            title_hit = self.set_title_hit(hash_terms, hash_curr_qry_titles)
            # if title_hit == 301:
            #     self.hash_view[doc_id] = hash_terms
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
                try:
                    max_tf_d = self.hash_doc_data[doc_id][0]
                except Exception:
                    max_tf_d = 1
                # tf_q = value[0] / qry_max_tf
                # tf_d = value[1] / max_tf_d
                # tf_d = 1 / value[1]
                tf_q = value[0]
                tf_d = value[1] * max_tf_d
                idf = value[2]
                h = value[3]
                nmr = (self.k + 1) * tf_d + (self.h_const * h)
                dnmr = tf_d + self.k * (1 - self.b + (self.b * (doc_size / self.avgdl)))
                fraction = nmr / dnmr
                # value = (tf_q * term_hit) * fraction * idf
                value = tf_q * (self.l + fraction) * idf
                bm25 += value
            # tuple_results = tuple_results + (doc_id, bm25)
            if bm25 > 0:
                bm25 = float("{0:.5f}".format(bm25 * title_hit * self.w_bm25))
                # tuple_results.append((doc_id, bm25))
                self.hash_results[doc_id] = bm25

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

    def start_rank_cossim(self, hash_docs, qry_max_tf, qry_id, sigma_w_ij):
        hash_curr_qry_titles = self.hash_titles[qry_id]
        tf_ttl_q = len(hash_curr_qry_titles)
        sigma_w_iq = tf_ttl_q
        for doc_id, hash_terms in hash_docs.items():
            cossim = 0
            nmr = 0
            for term, value in hash_terms.items():
                tf_q = value[0]
                tf_d = value[1]
                idf = value[2]
                h = value[3]
                tf_q_sum = ((tf_ttl_q * tf_q) / qry_max_tf)
                nmr += tf_q_sum * tf_d * idf + (self.h_const * h)
            sigma_w_ij = self.hash_doc_data[doc_id][1]
            dnmr = sqrt(sigma_w_ij * sigma_w_iq)
            cossim = float("{0:.5f}".format((nmr / dnmr) * self.w_cossim))
            if cossim > 0:
                try:
                    self.hash_results[doc_id] += cossim
                except Exception:
                    self.hash_results[doc_id] = cossim

    def start_filter_results(self):
        tuple_results = sorted(self.hash_results.items(), key=lambda kv: kv[1])
        if len(tuple_results) > 50:
            tuple_results = tuple_results[0:50]
        # tuple_results = sorted(tuple_results, key=lambda tup: tup[1])
        # tuple_results = sorted(tuple_results, key=lambda tup: (-tup[1], tup[0]))
        # if len(tuple_results) > 1000:
        #     tuple_results = tuple_results[0:1000]
        # return tuple_results
        return tuple_results
