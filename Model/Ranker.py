

class Ranker:

    def __init__(self, max_tf, b):
        self.k = max_tf
        self.b = b

    def start_rank(self, hash_docs, doc_size, doc_avg):
        tuple_results = []
        for doc_id, hash_terms in hash_docs.items():
            bm25 = 0
            for term, value in hash_terms.items():
                tf_q = value[0]
                tf_d = value[1]
                idf = value[2]
                h = value[3]
                bm25 += float("{0:.4f}".format((tf_q * (((self.k + 1) * tf_d) /
                                 (tf_d + (self.k * (1 - self.b + (self.b * (doc_size / doc_avg)))))) * idf)))
            tuple_results.append((doc_id, bm25))
        # tuple_results = sorted(tuple_results, key=lambda tup: tup[1])
        tuple_results = sorted(tuple_results, key=lambda tup: (-tup[1], tup[0]))
        return tuple_results

