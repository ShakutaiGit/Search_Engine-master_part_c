import utils

# DO NOT MODIFY CLASS NAME
class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.doc_counter = 0
        self.inverted_idx = {}
        self.postingDict = {}
        self.docs_dict = {}
        self.config = config
        self.pop_dict = {}
        self.thresh_hold = 125000
        self.stop_cleaning_value = 100000
        self.exponent_grown_word_size_to_remove = 4

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        document_dictionary = document.term_doc_dictionary
        self.simple_dics_combine(document_dictionary, document.entity_dict)
        max_tf = self.update_inverted(document_dictionary,document.tweet_id)
        length = len(document_dictionary)
        self.save_information_on_doc(length, max_tf, document.tweet_id, document.tweet_date, document.retweet)
        self.doc_counter += 1
        self.thresh_hold_handler()

    def thresh_hold_handler(self):
        if self.thresh_hold < len(self.inverted_idx):
            while self.stop_cleaning_value < len(self.inverted_idx):
                to_remove = self.get_list_of_terms_to_remove()
                self.clean_inverted_to_thresh_hold(to_remove)
                self.exponent_grown_word_size_to_remove = self.exponent_grown_word_size_to_remove*2
            self.exponent_grown_word_size_to_remove = self.exponent_grown_word_size_to_remove / 2

    def clean_inverted_to_thresh_hold(self, remove_list):
        for remove_item in remove_list:
            self.inverted_idx.pop(remove_item)
            self.postingDict.pop(remove_item)
            if self.stop_cleaning_value >= len(self.inverted_idx):
                break

    def get_list_of_terms_to_remove(self):
        res = []
        for key, value in self.inverted_idx.items():
            if value < self.exponent_grown_word_size_to_remove:
                res.append(key)
        return res

    def save_information_on_doc(self, unique, max_tf, tweet_id, tweet_date, rt_list):
        self.simple_dics_combine(self.pop_dict, rt_list)
        self.docs_dict[tweet_id] = (max_tf, unique, tweet_date[0])

    def simple_dics_combine(self, source, to_add):
        for key in to_add.keys():
            if key in source:
                source[key] += to_add[key]
            else:
                source[key] = to_add[key]

    def calculate_posting_terms(self):
        count = 0
        for term in self.postingDict:
            count += len(self.postingDict[term])
        return count

    def posting_small_letter_handler(self, key, value, tweet_id):
        opp_word = key.upper()
        if opp_word in self.postingDict:
            self.postingDict[key] = [(tweet_id, value)]
            self.postingDict[key] += self.postingDict[opp_word]
            self.postingDict.pop(opp_word)
        else:
            self.adding_to_posting(key, value, tweet_id)

    def posting_big_letters_handler(self, key, value, tweet_id):
        opp_word = key.lower()
        if opp_word in self.postingDict:
            self.adding_to_posting(opp_word, value, tweet_id)
        else:
            self.adding_to_posting(key, value, tweet_id)

    def adding_to_posting(self, key, value, tweet_id):
        if key in self.postingDict:
            self.postingDict[key] += [(tweet_id, value)]
        else:
            self.postingDict[key] = [(tweet_id, value)]

    def update_inverted(self, dict_to_combine, tweet_id):
        max_val = 0
        for key, value in dict_to_combine.items():
            if value > max_val:
                max_val = value
            if key in self.inverted_idx:
                self.inverted_idx[key] += value
                self.adding_to_posting(key, value, tweet_id)
            elif key[0].isupper():
                self.inverted_big_letters_handler(key, value)
                self.posting_big_letters_handler(key, value, tweet_id)
            elif key[0].islower():
                self.inverted_small_letter_handler(key, value)
                self.posting_small_letter_handler(key, value, tweet_id)
            else:
                self.inverted_idx[key] = value
                self.adding_to_posting(key, value, tweet_id)
        return max_val

    def inverted_small_letter_handler(self, key, value):
        opp_word = key.upper()
        if opp_word in self.inverted_idx:
            self.inverted_idx[key] = value + self.inverted_idx[opp_word]
            self.inverted_idx.pop(opp_word)

        else:
            self.inverted_idx[key] = value

    def inverted_big_letters_handler(self, key, value):
        opp_word = key.lower()
        if opp_word in self.inverted_idx:
            self.inverted_idx[opp_word] += value
        else:
            self.inverted_idx[key] = value

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        saved_files = utils.load_obj(fn)
        return saved_files

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        utils.save_obj((self.inverted_idx,self.postingDict,self.pop_dict),fn)

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.inverted_idx

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        if term in self.postingDict:
            return self.postingDict[term]
        return None

