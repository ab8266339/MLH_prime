import re
import numpy as np

class Miscellaneous(object):
    
    @staticmethod
    def ConvertStrToBagOfWords(reg, reg_exclude, document_in_a_sentence):

        # find all words match regular expression
        document_word_list = re.findall(reg, document_in_a_sentence)

        return document_word_list
    
    @staticmethod
    #input word_dict = {'word1':2, 'word2': 9}, converted to ndarray in order
    def DictToNdarray(word_dict):
        sorted_value_list = [word_dict[x] for x in sorted(word_dict)]
        word_array = np.array([sorted_value_list])
        return word_array