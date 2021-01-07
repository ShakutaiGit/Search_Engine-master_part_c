
from nltk.corpus import wordnet
# import nltk
# nltk.download('wordnet')


class WordNet:
    def __init__(self, indexer):
        self.indexer = indexer
        # self.thresh_hold = self.thresh_hold_calculator()

    # def thresh_hold_calculator(self):
    #     print("to implement")
    #     return 100

    def query_expan(self, query_terms):
        expand_terms = []
        # term_to_expan = self.which_terms_to_expan(query_terms)
        for term in query_terms:
            expand_term = self.expan_to_different_term(term)
            if not expand_term is None:
                expand_terms.append(expand_term)
        return expand_terms

    def expan_to_different_term(self,term):

        for syn in wordnet.synsets(term):
            for l in syn.lemmas():
                if not l.name() == term:
                    return l.name()

    # def which_terms_to_expan(self,query_terms):
    #     res_terms = []
    #     for term in query_terms:
    #         if term not in self.indexer.inverted_idx:
    #             res_terms.append(term)
    #         elif self.indexer.inverted_idx[term] <= self.thresh_hold_calculator():
    #             res_terms.append(term)
    #     return res_terms