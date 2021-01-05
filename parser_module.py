import json
import math
import re
import string
import unicodedata
from nltk.corpus import stopwords
from document import Document
from stemmer import Stemmer

stemmer = Stemmer()


class Parse:

    def __init__(self, stemmer):
        self.tens = {'Thousand': 'k', 'Million': 'M', 'Billion': 'B', 'thousand': 'K', 'million': 'M', 'billion': 'B'}
        self.panctuation_to_remove = ['*', '!', '&', '“', '‘', '(', ')', '+', '...', '.', '/', ':', ';', '"', '<', '=',
                                      '>', '?', '[', ']', '^', '`', '{', '|', '}', '~', "'"]
        self.monthes = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                        'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        self.panctuation_to_space = ['&', '_', '-']
        self.url_panct = ['http', 'https', 'i', 'web', 'www', 'status', 't.co', 'twitter.com']
        self.percent = {'percent', 'percentage', 'Percentage', 'Percent'}
        self.stop_words = stopwords.words('english')
        self.upper_word = []
        self.entity_dict = {}
        self.retweet_dict = {}
        self.stemmer_status = stemmer
        self.url = None

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        final_terms = []
        entity = []
        entity_index = None
        text_no_emoji = self.remove_emoji(text)  # take alots of time
        tokenize_text = self.tokenizer(text_no_emoji)

        for count, word in enumerate(tokenize_text, 0):
            word = ''.join([i for i in word if ord(i) < 128])  # remove latine and icons
            length_all_word = len(tokenize_text)
            if word == '' or word == ' ':  # remove if the word empty
                continue
            if 'http' in word:  # maybe change
                self.url = word
                continue
            elif '-' in word:
                split_word = word.split('-')
                tokenize_text.extend(split_word)
            elif '_' in word:
                clean_word = self.under_line_handler(word)
                tokenize_text.extend(clean_word)
            elif '/' in word:
                clean_word = self.diagonal_line_handler(word)
                tokenize_text.extend(clean_word)
            elif '%' in word:  # deal with % need to fix
                punctuation = ['&lt;', '~', '(', ')', '"', '~', '?', ':']
                word_punctuation = self.replaceMultiple(word, punctuation, '')
                if len(word_punctuation) > 1:
                    final_terms.append(word_punctuation)
                else:
                    continue
            elif word[0] == '$' or word[len(word) - 1] == '$':
                term = self.dolar_handler(word)
                if not term == None:
                    final_terms.append(word)
            elif word.isnumeric():  # deal with numers and percent
                term = self.numeric_handler(word, count, tokenize_text, length_all_word)
                if not term == None:
                    final_terms.append(term)
            else:
                word_punctuation = self.replaceMultiple(word, self.panctuation_to_remove, '')
                if '@' in word_punctuation:
                    if word_punctuation.index('@') == 0 and len(word_punctuation) > 1:
                        final_terms.append(word_punctuation)
                elif '#' in word_punctuation:
                    if word_punctuation.index('#') == 0 and len(word_punctuation) > 1:
                        new_word = word_punctuation.replace('#', '')
                        list_of_terms = self.hash_tags_Handler(new_word)
                        final_terms.extend(list_of_terms)
                else:
                    if len(word_punctuation) > 2:
                        if word_punctuation[0].isupper():  # make upper dict and entity
                            final_terms.append(word_punctuation.upper())
                            if entity_index is None or count == entity_index + 1:
                                entity.append(word_punctuation)
                                entity_index = count
                            else:
                                if len(entity) > 1:
                                    self.push_to_entity_dict(entity)
                                entity.clear()
                                entity.append(word_punctuation)
                                entity_index = count
                        else:  # deal with other words
                            if not word_punctuation in self.stop_words:
                                lower_word = word_punctuation.lower()
                                final_terms.append(self.words_handler(lower_word))

        if len(entity) > 1:
            self.push_to_entity_dict(entity)
        # if not len(self.upper_word) == 0:
        #     final_terms.extend(self.small_and_big_letters_dicts_update(self.upper_word, final_terms))

        return final_terms, self.entity_dict

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-presenting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text, entity_dict = self.parse_sentence(full_text)
        tweet_date = self.tweet_date_parse(tweet_date)

        # url parser
        url_parse = []
        if len(url) > 2:
            url_json = json.loads(url)
            val = url_json.popitem()
            if val[1] == None:
                url_parse = (self.url_Handler(val[0], tweet_id))
            else:
                url_parse = (self.url_Handler(val[1], tweet_id))
        else:
            if not self.url == None:
                url_parse = (self.url_Handler(self.url, tweet_id))
        if len(url_parse) > 0:
            tokenized_text.extend(url_parse)

        # find the retweet to calc popularity
        res = [doc_as_list[6], doc_as_list[9], doc_as_list[12]]
        self.popularety_retweet(res, tweet_id)

        doc_length = len(tokenized_text)  # after text operations.
        # tokenized_text.extend(self.small_and_big_letters_dicts_update(self.upper_word, tokenized_text))

        for term in tokenized_text:
            if not term == '' or not term == ' ':
                if term not in term_dict.keys():
                    term_dict[term] = 1
                else:
                    term_dict[term] += 1

        # term_dict = self.small_and_big_letters_dicts_update(self.dict_upper_word, term_dict)
        # print("tokenized_text: {} ".format(term_dict))
        # print("pop:{}".format(self.retweet_dict))
        # print("entity:{}".format(entity_dict))

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length, entity_dict.copy(), self.retweet_dict.copy())

        self.entity_dict.clear()
        self.retweet_dict.clear()
        return document

    def popularety_retweet(self,url_list,id_tweet):
        for url in url_list:
            url_parse = []
            if not url==None and not url == '{}':
                url_json = json.loads(url)
                val = url_json.popitem()
                if not val[1] == None:
                    url_parse = val[1].split('/')
                if len(url_parse) > 0:
                    id_RT = url_parse.pop(len(url_parse) - 1)
                    if id_RT.isnumeric():
                        if not id_RT in self.retweet_dict and not id_RT == id_tweet:
                            self.retweet_dict[id_RT] = 1

    def under_line_handler(self,word):
        clean_word = word.replace('_',' ')
        list_no_underline = clean_word.split(' ')
        return list_no_underline

    def diagonal_line_handler(self,word):
        clean_word = word.replace('/',' ')
        list_no_underline = clean_word.split(' ')
        return list_no_underline

    def tweet_date_parse(self,tweet_date):
        date_term = tweet_date.split()
        month = self.monthes[date_term[1]]
        date = date_term[2]+'/'+month+'/'+date_term[5]
        date_time = [date,date_term[3]]
        return date_time

    def dolar_handler(self,word):
        no_dolar = word.replace('$','')
        dolar_panc = ['(',')','?',':','['']','!','/',]

        if len(no_dolar) > 0 and no_dolar[0].isnumeric():
            clean_term = self.replaceMultiple(no_dolar,dolar_panc,'')
            with_dolar = '$'+clean_term
            return with_dolar
        else:
            return None

    def words_handler(self, word):
        if self.stemmer_status:
            if word[0].isupper():
                word = stemmer.stem_term(word)
            else:
                word = word.lower()
                word = stemmer.stem_term(word)
        return word

    def numeric_handler(self, word,index_of_word, all_words,length_all_word):
        if not word.isdigit():
            return word
        if self.check_digit(word): #mayby else
            float_number = self.to_float(word)
            if length_all_word > index_of_word + 1:
                next_word = all_words[index_of_word + 1]
                if next_word in self.tens:
                    check_number = self.numbers_to_unit_rull(float_number, next_word)
                elif next_word in self.percent:
                    check_number = str(float_number)+'%'
                else:
                    check_number = self.numbers_to_unit_rull(float_number)
            else:
                check_number = self.numbers_to_unit_rull(float_number)
            return check_number


    def hash_tags_Handler(self, text):
        new_list=[]
        if '_' in text:
            term_list = re.split('_', text)
        else:
            term_list = re.findall(r"[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])", text)
        new_list.append("#" + text.lower())
        for item in term_list:
            if len(item) > 1:
                lower_term = self.words_handler(item.lower())
                new_list.append(lower_term)
        return new_list

    def tokenizer(self,text):
        char_to_replace = ['—','\n','…',',','...']
        text_to_space = self.replaceMultiple(text,char_to_replace , ' ')
        new_text = text_to_space.replace(',','')
        tokenize_text = new_text.split(" ")
        return tokenize_text

    def replaceMultiple(self,mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces:
            # Check if string is in the main string
            if elem in mainString:
                # Replace the string
                mainString = mainString.replace(elem, newString)
        return mainString

    def numbers_to_unit_rull(self, number,text=None):
        if number < 1000:
            number = number
        number = float('{:.5g}'.format(math.modf(number)[1]))
        magnitude = 0
        while abs(number) >= 1000:
            magnitude += 1
            number /= 1000.0
        if magnitude > 4:
            magnitude = 4
        if text is None:
            return '{}{}'.format('{:f}'.format(number).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
        else:
            numeric_term = '{}{}'.format('{:f}'.format(number).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
            return numeric_term+self.tens[text]


    def url_Handler(self, url_sentence,tweet_id):
        TermsToSave = []
        parse_url = re.split('[/@!$#(),;+?%=~*&:]',url_sentence)
        for term in parse_url:
            if '-' in term:
                new_term = term.split('-')
                parse_url.extend(new_term)
            elif len(term) >1:
                if 'www' in term:
                    term = term.replace('www.','')
                if len(term)>1 and not term == tweet_id:
                    if not term in self.url_panct:
                        lower_term = term.lower()
                        TermsToSave.append(lower_term)
        return TermsToSave

    def remove_emoji(self,text):
        regrex_pattern = re.compile(pattern="["
                                               "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                                "\U0001F300-\U0001F5FF"  # symbols & pictographs
                                                "\U0001F600-\U0001F64F"  # emoticons
                                                "\U0001F680-\U0001F6FF"  # transport & map symbols
                                                "\U0001F700-\U0001F77F"  # alchemical symbols
                                                "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                                                "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                                                "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                                                "\U0001FA00-\U0001FA6F"  # Chess Symbols
                                                "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                                                "\U00002702-\U000027B0"  # Dingbats
                                                "\U000024C2-\U0001F251"
                                            "]+", flags=re.UNICODE)
        no_emoji = regrex_pattern.sub(r'',text)
        return no_emoji

    def small_and_big_letters_dicts_update(self, upper_letters, all_terms):
        add_to_final =[]
        for word in upper_letters:
            term_to_lowers = word.lower()
            if term_to_lowers in all_terms:
                add_to_final.append(term_to_lowers)
            else:
                add_to_final.append(word.upper())
        return add_to_final

        # for term in upper_letters.keys():
        #     term_to_lowers = term.casefold()
        #     if term_to_lowers in dict_to_check:
        #             dict_to_check[term_to_lowers] += upper_letters[term]
        #     else:
        #             dict_to_check[term] = upper_letters[term]
        # self.dict_upper_word.clear()
        # return dict_to_check

    def check_digit(self, word):
        for letter in word:
            if letter not in string.digits:
                return False
        return True

    def to_float(self,word):
        if len(word) == 1:
            return unicodedata.numeric(word)
        elif word[-1].isdigit():
            return float(word)
        else:
            # Assume the last character is a vulgar fraction
            return float(word[:-1]) + unicodedata.numeric(word[-1])

    def push_to_upper_dict(self,word_punctuation):
        word_lower = word_punctuation.lower()
        if not word_lower in self.stop_words:
            if word_punctuation.upper() in self.dict_upper_word:
                self.dict_upper_word[self.words_handler(word_punctuation.upper())] += 1
            else:
                self.dict_upper_word[self.words_handler(word_punctuation.upper())] = 1

    def push_to_entity_dict(self,entity):

        final_entity = (' '.join([str(elem) for elem in entity]))
        if final_entity in self.entity_dict:
            self.entity_dict[final_entity] += 1
        else:
            self.entity_dict[final_entity] = 1
