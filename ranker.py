# you can change whatever you want in this module, just make sure it doesn't 
# break the searcher module

from inner_product import Inner_product


class Ranker:
    def __init__(self, indexer):
        self.docs_limit = 2000
        self.indexer = indexer
        self.max_pop = max(self.indexer.pop_dict)

    def rank_relevant_docs(self, relevant_doc, relevant_terms):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        inner_product = Inner_product(relevant_doc, relevant_terms, self.indexer)
        ranked = inner_product.rank()
        self.pop_handler(ranked)
        rank_relevant_doc = sorted(ranked.items(), key=lambda item: item[1], reverse=True)
        return rank_relevant_doc

    def pop_handler(self, inner_prod):
        for term in inner_prod.keys():
            if term in self.indexer.pop_dict:
                norm_val = self.normelize_popularity(self.indexer.pop_dict[term])
                inner_prod[term] += norm_val

    def normelize_popularity(self, val):
        min_val = 0
        norm = 15 * ((val - min_val) / (self.max_pop - min_val)) + 1
        return norm

    def retrieve_top_k(self, sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        if k > self.docs_limit:
            k = self.docs_limit
        return sorted_relevant_doc[:k]
