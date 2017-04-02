import re
import numpy as np

class Miscellaneous(object):
    
    @staticmethod
    def ConvertStrToBagOfWords(reg, reg_exclude, document_in_a_sentence):
        document_word_list = []
        # find all words match regular expression
        word_list_before_filter = re.findall(reg, document_in_a_sentence)
        #exclude all invalid words
        word_list = []
        for i,word in enumerate(word_list_before_filter):
            try:
                find_excluded = re.findall(reg_exclude, word)
            # if the reg is invalid, print the details 
            except TypeError:
                print ("error word: ", word)
            #not found means the word should not be excluded and should be added to list
            if not find_excluded:
                word_list.append(word)
            
        document_word_list.extend(word_list)
        return document_word_list
    
    @staticmethod
    #input word_dict = {'word1':2, 'word2': 9}, converted to ndarray in order
    def DictToNdarray(word_dict):
        sorted_value_list = [word_dict[x] for x in sorted(word_dict)]
        word_array = np.array([sorted_value_list])
        return word_array