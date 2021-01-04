# DO NOT MODIFY CLASS NAME
class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.doc_counter = 0
        self.inverted_idx = {}
        self.postingDict = {}
        self.init_posting_files()
        self.config = config
        self.pop_dict = {}

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
        max_tf = self.update_inverted(document_dictionary)
        self.update_posting()
        length = len(document_dictionary)
        self.save_information_on_doc(length, max_tf, document.tweet_id, document.tweet_date, document.retweet)
        self.doc_counter += 1

    def save_information_on_doc(self, unique, max_tf, tweet_id, tweet_date, rt_list):
        self.simple_dics_combine(self.pop_dict, rt_list)
        self.postingDict["docs"][tweet_id] = (max_tf, unique, tweet_date[0])

    def simple_dics_combine(self, source, to_add):
        for key in to_add.keys():
            if key in source:
                source[key] += to_add[key]
            else:
                source[key] = to_add[key]

    def update_posting(self, dict_to_combine, tweet_id):
        for key, value in dict_to_combine.items():
            if key[0] is '$' or '%' in key or key[0].isnumeric():
                self.adding_to_posting("numbers", key, value, tweet_id)
            elif key[0].isupper():
                self.posting_big_letters_handler(key, value, tweet_id)
            elif key[0].islower():
                self.posting_small_letter_handler(key, value, tweet_id)
            elif key[0] is '#' or key[0] is '@':
                self.adding_to_posting(key[0], key, value, tweet_id)

    def posting_small_letter_handler(self, key,value, tweet_id):
        opp_word = key.upper()
        if opp_word in self.postingDict[key[0]]:
            self.postingDict[key[0]][key] = [(tweet_id,value)]
            self.postingDict[key[0]][key] += self.postingDict[key[0]][opp_word]
            self.postingDict[key[0]].pop(opp_word)
        else:
            self.adding_to_posting(key[0], key.value, tweet_id)

    def posting_big_letters_handler(self, key, value, tweet_id):
        opp_word = key.lower()
        if opp_word in self.postingDict[opp_word[0]]:
            self.adding_to_posting(opp_word[0], opp_word, value, tweet_id)
        else:
            self.adding_to_posting(key[0], opp_word, value, tweet_id)

    def adding_to_posting(self, category, key, value, tweet_id):
        if key in self.postingDict[category]:
            self.postingDict[category][key] += [(tweet_id, value)]
        else:
            self.postingDict[category][key] = [(tweet_id, value)]

    def update_inverted(self, dict_to_combine):
        max_val = 0
        for key, value in dict_to_combine.items():
            if value > max_val:
                max_val = value
            if key in self.inverted_idx:
                self.inverted_idx[key] += value
            elif key[0].isupper():  # now i have to check if the casefold word is in the inverted idx if it does i have to combine this value
                self.inverted_big_letters_handler(key, value)
            elif key[0].islower():
                self.inverted_small_letter_handler(key, value)
            else:
                self.inverted_idx[key] = value
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
        raise NotImplementedError

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        raise NotImplementedError

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
        first_letter = term[0].lower()
        if first_letter in self.postingDict and term in self.postingDict[first_letter]:
            return self.postingDict[first_letter][term]
        return None

    def init_posting_files(self):
        ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        for char in ascii_lowercase:
            self.postingDict[char] = {}
        self.postingDict["#"] = {}
        self.postingDict["@"] = {}
        self.postingDict["numbers"] = {}
        self.postingDict["docs"] = {}
        self.postingDict["entitys"] = {}
