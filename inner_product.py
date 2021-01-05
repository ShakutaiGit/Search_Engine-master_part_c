import json
import math

from indexer import Indexer
import utils
class Inner_product:

    def __init__(self, relevant_docs, terms_dict, indexer):
        self.relevant_docs = relevant_docs #all the relevant docs with out duplicates and counter of the words
        self.terms = terms_dict # dict of lists from posting for each term
        self.corp_size = len(indexer.inverted_idx)
        self.indexer = indexer
        self.max_tf = {}

    #indexer tuple (idx , posting , docs , pop)
    def get_max_f_for_relevant_docs(self):
        for key in self.relevant_docs.keys():
            value = self.indexer.docs_dict[key][0]
            self.max_tf[key] = value

    def calculate_tf(self, f, id_doc):
        max_f = self.max_tf[id_doc]
        return f/max_f

    def calculate_idf(self,df):
        cal = self.corp_size / df
        return math.log(cal,2)

    def rank(self):
        self.get_max_f_for_relevant_docs()
        tf_idf_for_id = {}
        for key,val in self.terms.items():
            df = len(val)
            for item in val:
                f_in_doc = item[1]
                tf_word = self.calculate_tf(f_in_doc, item[0])
                idf_word = self.calculate_idf(df)
                tf_idf = tf_word*idf_word
                if item[0] in tf_idf_for_id:
                    tf_idf_for_id[item[0]].append(tf_idf)
                else:
                    tf_idf_for_id[item[0]] = [tf_idf]

        rank = {}
        for key, val in tf_idf_for_id.items():
            rank[key] = sum(val)
        return rank































