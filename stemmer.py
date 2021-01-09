from nltk.stem import snowball
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


class Stemmer:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def stem_term(self, token):
        """
        This function stem a token
        :param token: string of a token
        :return: stemmed token
        """
        return self.stemmer.stem(token)

class Lemmatizer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def lemm_term(self, token):
        """
        This function stem a token
        :param token: string of a token
        :return: stemmed token
        """
        return self.lemmatizer.lemmatize(token)

