

class Ranker:

    def __init__(self, max_tf, b):
        self.k = max_tf
        self.b = b

    def start_rank(self, hash_qry, hash_index):
        for qry_key, qry_val in hash_qry.items():
            for term, tf_q in qry_val.items():
                w_qry_term = tf_q
