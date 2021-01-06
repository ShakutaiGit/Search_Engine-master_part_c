from nltk.corpus import wordnet
class WordNet:
    def __init__(self, indexer):
        self.indexer = indexer
        self.thresh_hold = self.thresh_hold_calculator()

    def thresh_hold_calculator(self):
        print("to implement")
        return 100

    def query_expan(self, query_terms):
        term_to_expan = self.which_terms_to_expan(query_terms)
        for term in term_to_expan:
            synset = wordnet.synsets(term)
            query_terms.append(synset[0].lemmas()[0].name())# maybe here we need to make some selecting from the options
        return query_terms

    def which_terms_to_expan(self,query_terms):
        res_terms = []
        for term in query_terms:
            if term not in self.indexer.inverted_idx:
                res_terms.append(term)
            elif self.indexer.inverted_idx[term] <= self.thresh_hold_calculator():
                res_terms.append(term)
        return res_terms