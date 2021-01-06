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
        #parse the query and get list of term, list of entity
        query_as_list, entity_dict = self._parser.parse_sentence(query)
        entity_as_list = list(entity_dict.keys())
        #get the relevant docs id, info of relevant term
        relevant_docs_query, relevant_terms_query = self._relevant_docs_from_posting(query_as_list)
        relevant_docs_entity, relevant_terms_entity = self._relevant_docs_to_entity(entity_as_list)

        #combine dict of docs and entity
        full_relevant_doc = {**relevant_docs_query,**relevant_docs_entity}
        full_relevant_term = {**relevant_terms_query,**relevant_terms_entity}

        n_relevant = len(full_relevant_doc)
        #start ranker
        ranked_doc_ids = self._ranker.rank_relevant_docs(relevant_doc=full_relevant_doc, relevant_terms=full_relevant_term)
        return n_relevant, ranked_doc_ids

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        relevant_terms = {}
        relevant_docs = {}
        for term in query_as_list:
            posting_list_of_term = []
            #if term is numeric get term info
            if term.isnumeric():
                    list = self._indexer.get_term_posting_list(term)
                    if not list is None:
                        posting_list_of_term.extend(list)
            else:#if term no numeric get info to upper&lower
                    list = self._indexer.get_term_posting_list(term)
                    if not list is None:
                        posting_list_of_term.extend(list)
                    list= self._indexer.get_term_posting_list(term.casefold())
                    if not list is None:
                        posting_list_of_term.extend(list)
            #add to relevant doc and save the info of term
            for doc_id in posting_list_of_term:
                if doc_id in relevant_docs:
                    relevant_docs[doc_id[0]] +=1
                else:
                    relevant_docs[doc_id[0]] = 1
                relevant_terms[term] = posting_list_of_term
        return relevant_docs, relevant_terms

    def _relevant_docs_to_entity(self, entity_as_list):
        relevant_docs = {}
        relevant_terms = {}
        for term in entity_as_list:
            posting_list = self._indexer.get_term_posting_list(term)
            if not posting_list is None:
                for doc_id, tf in posting_list:
                    df = relevant_docs.get(doc_id, 0)
                    relevant_docs[doc_id] = df + 1
                    relevant_terms[term] = posting_list
        return relevant_docs, relevant_terms


