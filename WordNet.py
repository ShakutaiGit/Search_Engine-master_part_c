
from nltk.corpus import wordnet
# import nltk
# nltk.download('wordnet')


class WordNet:
    def __init__(self, indexer):
        self.indexer = indexer
        # self.thresh_hold = self.thresh_hold_calculator()

    # def thresh_hold_calculator(self):
    #     return 100

    def query_expan(self, query_terms):
        expand_terms = []
        # term_to_expan = self.which_terms_to_expan(query_terms)
        for term in query_terms:
            candidate_terms = self.expan_to_different_term(term)
            for t in candidate_terms:
                if t is not None:
                    expand_terms.append(t)
        return expand_terms

    def expan_to_different_term(self,term):
        num_of_terms = 2
        results = []
        for syn in wordnet.synsets(term):
            for l in syn.lemmas():
                if num_of_terms is 0:
                    break;
                if not l.name() == term:
                   results.append(l.name())
                   num_of_terms += -1
        return results