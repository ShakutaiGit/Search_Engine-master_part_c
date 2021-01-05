from ranker import Ranker
import utils


# DO NOT MODIFY CLASS NAME
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model 
    # parameter allows you to pass in a precomputed model that is already in 
    # memory for the searcher to use such as LSI, LDA, Word2vec models. 
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker(indexer)
        self._model = model

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=None):
        """ 
        Executes a query over an existing index and returns the number of 
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and 
            a list of tweet_ids where the first element is the most relavant 
            and the last is the least relevant result.
        """
        query_as_list, entity_dict = self._parser.parse_sentence(query)
        entity_as_list = list(entity_dict.keys())

        relevant_docs_query = self._relevant_docs_from_posting(query_as_list)
        relevant_docs_entity = self._relevant_docs_to_entity(entity_as_list)
        full_relevant = {**relevant_docs_query,**relevant_docs_entity}
        n_relevant = len(full_relevant)
        ranked_doc_ids = Ranker.rank_relevant_docs(full_relevant)
        return n_relevant, ranked_doc_ids

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        relevant_docs = {}
        for term in query_as_list:
            posting_list = []
            if term.isnumeric():
                    list = self._indexer.get_term_posting_list(term)
                    if not list is None:
                        posting_list.extend(list)
            else:
                    list = self._indexer.get_term_posting_list(term)
                    if not list is None:
                        posting_list.extend(list)
                    list= self._indexer.get_term_posting_list(term.casefold())
                    if not list is None:
                        posting_list.extend(list)
            if not posting_list is None:
                for doc_id, tf in posting_list:
                    df = relevant_docs.get(doc_id, 0)
                    relevant_docs[doc_id] = df + 1
        return relevant_docs

    def _relevant_docs_to_entity(self, entity_as_list):
        relevant_docs = {}
        for term in entity_as_list:
            posting_list = self._indexer.get_term_posting_list(term)
            if not posting_list is None:
                for doc_id, tf in posting_list:
                    df = relevant_docs.get(doc_id, 0)
                    relevant_docs[doc_id] = df + 1
        return relevant_docs

