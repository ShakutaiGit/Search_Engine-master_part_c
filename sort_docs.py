
class Sorts:
    def __init__(self, indexer, ):
        self.indexer = indexer

    def sort_by_time(self, relevant_docs):
        time_relevant_dict = {}
        for doc in relevant_docs:
            info_doc = self.indexer.docs_dict[doc]
            time_relevant_dict[doc] = info_doc[2]
        sorted_doc = sorted(time_relevant_dict.items(), key=lambda item: item[1], reverse=True)
        return sorted_doc

    def sort_by_pop(self,relevant_docs):
        pop_relevant_dict = {}
        for doc in relevant_docs:
            pop_dict = self.indexer.pop_dict
            if doc in pop_dict.keys():
                pop_doc = self.indexer.pop_dict[doc]
                pop_relevant_dict[doc] = pop_doc
            else:
                pop_relevant_dict[doc] = 0
        sorted_doc = sorted(pop_relevant_dict.items(), key=lambda item: item[1], reverse=True)
        return sorted_doc







