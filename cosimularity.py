import math

from inner_product import Inner_product

class Cosimularity:

    def __init__(self, relevant_docs, terms_dict, indexer):
        self.relevant_docs = relevant_docs #all the relevant docs with out duplicates and counter of the words
        self.terms = terms_dict # dict of lists from posting for each term
        self.corp_size = len(indexer.inverted_idx)
        self.indexer = indexer
        self.max_tf = {}


    def rank(self,qury_terms):
        inner_product = Inner_product(self.relevant_docs,self.terms,self.indexer)
        inner_calc = inner_product.rank()
        query = len(qury_terms)
        rank = {}
        for doc in self.relevant_docs.keys():
            sum_terms_w = 0
            max_f_doc = self.indexer.docs_dict[doc][0]#the max term in doc
            terms_doc_dict = self.indexer.docs_dict[doc][3]#all terms in doc

            for term,term_show in terms_doc_dict.items():
                if term in self.indexer.inverted_idx:
                    f_term = term_show #show term in doc
                    tf_term = f_term/max_f_doc
                    term_info = self.indexer.postingDict[term]
                    df = len(term_info)#how many docs the term show
                    idf_term = inner_product.calculate_idf(df)
                    tf_idf_term = tf_term * idf_term
                    tf_idf_pow = tf_idf_term **2
                    sum_terms_w +=tf_idf_pow
                else:
                    continue
            vector_size = math.sqrt(sum_terms_w * query)
            rank[doc] = (inner_calc[doc] / vector_size)

        return rank






