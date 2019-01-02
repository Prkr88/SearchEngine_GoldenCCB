from numpy import sqrt


class Ranker:

    hash_doc_data = {}
    hash_titles = {}
    hash_view = {}
    hash_results = {}
    hash_cos_data = {}

    def __init__(self, k, avgdl, M, hash_doc_data, hash_cos_data):
        # self.k = k
        self.k = 2
        self.avgdl = avgdl
        self.N = 472350
        self.b = 0.5
        self.l = 0.2
        self.h_const = 10
        self.w_bm25 = 0.05
        self.w_cossim = 0.95
        self.hash_doc_data = hash_doc_data
        self.hash_cos_data = hash_cos_data
        self.title_hit_bonus = 5
        self.title_hit_fine = 0.05
        self.term_hit_bonus = 5
        self.term_hit_fine = 1

    def set_hash_titles(self, hash_titles):
        self.hash_titles = hash_titles

    def start_rank(self, hash_docs, qry_max_tf, qry_id):
        self.start_rank_bm25(hash_docs, qry_id)
        self.start_rank_cossim(hash_docs, qry_max_tf, qry_id)
        return self.start_filter_results()

    def start_rank_bm25(self, hash_docs, qry_id):
        for doc_id, hash_terms in hash_docs.items():
            title_hit = self.set_title_hit(hash_terms, qry_id)
            bm25 = 0
            try:
                doc_size = self.hash_doc_data[doc_id][2]
            except Exception:
                doc_size = self.avgdl
            for term, value in hash_terms.items():
                term_hit = self.set_term_hit(term, qry_id)
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
                # bm25 = float("{0:.5f}".format(bm25 * title_hit * self.w_bm25))
                bm25 = float("{0:.8f}".format(bm25 * self.w_bm25))
                # tuple_results.append((doc_id, bm25))
                if 'LA' in doc_id:
                    doc_id = self.doc_decompressor(doc_id)
                self.hash_results[doc_id] = bm25

    def set_term_hit(self, term, qry_id):
        hash_curr_qry_titles = self.hash_titles[qry_id]
        if term.lower() in hash_curr_qry_titles:
            return self.term_hit_bonus
        else:
            return self.term_hit_fine

    def set_title_hit(self, hash_terms, qry_id):
        hash_curr_qry_titles = self.hash_titles[qry_id]
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
                title_hit *= self.title_hit_bonus
            else:
                title_hit *= self.title_hit_bonus
        return title_hit

    def start_rank_cossim(self, hash_docs, qry_max_tf, qry_id):
        hash_curr_qry_titles = self.hash_titles[qry_id]
        tf_ttl_q = len(hash_curr_qry_titles)
        sigma_w_iq = tf_ttl_q
        for doc_id, hash_terms in hash_docs.items():
            title_hit = self.set_title_hit(hash_terms, qry_id)
            cossim = 0
            nmr = 0
            for term, value in hash_terms.items():
                tf_q = value[0]
                tf_d = value[1]
                idf = value[2]
                h = value[3]
                term_hit = self.set_term_hit(term, qry_id)
                tf_q_sum = ((tf_ttl_q * tf_q) / qry_max_tf)
                nmr += tf_q_sum * tf_d * idf + (self.h_const * h) + term_hit
                # nmr += tf_q_sum * tf_d * idf + (self.h_const * h)
            nmr += title_hit
            sigma_w_ij = self.hash_cos_data[doc_id]
            dnmr = sqrt(sigma_w_ij * sigma_w_iq)
            cossim = (nmr / dnmr) * self.w_cossim
            if cossim > 0:
                if 'LA' in doc_id:
                    doc_id = self.doc_decompressor(doc_id)
                try:
                    self.hash_results[doc_id] = float("{0:.8f}".format(self.hash_results[doc_id] + cossim))
                except Exception:
                    self.hash_results[doc_id] = float("{0:.8f}".format(cossim))

    def start_filter_results(self):
        tuple_results = sorted(self.hash_results.items(), key=lambda kv: kv[1], reverse=True)
        if len(tuple_results) > 1000:
            tuple_results = tuple_results[0:1000]
        # tuple_results = sorted(tuple_results, key=lambda tup: tup[1])
        # tuple_results = sorted(tuple_results, key=lambda tup: (-tup[1], tup[0]))
        # if len(tuple_results) > 1000:
        #     tuple_results = tuple_results[0:1000]
        # return tuple_results
        return tuple_results

    def set_params(self, title_hit_bonus, title_hit_fine, term_hit_bonus, term_hit_fine):
        self.title_hit_bonus = title_hit_bonus
        self.title_hit_fine = title_hit_fine
        self.term_hit_bonus = term_hit_bonus
        self.term_hit_fine = term_hit_fine
        # self.w_bm25 = w_bm25
        # self.w_cossim = w_cossim
        # self.h_const = h
        # self.b = b
        # self.l = l


    def doc_decompressor(self, doc_id):
        doc_list = doc_id.split('-')
        str_curr_id = doc_list[0]
        str_curr_gap = doc_list[1]
        zero_length = 4 - len(str_curr_gap)
        zero_str = ''
        for zero_index in range(0, zero_length):
            zero_str = zero_str + '0'
        str_curr_gap = zero_str + str_curr_gap
        doc_id = str_curr_id + '-' + str_curr_gap
        return doc_id