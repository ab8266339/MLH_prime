from miscellaneous import Miscellaneous
from FilterStopWords import FilterStopWords
from stemming import stemming
from nltk.stem import PorterStemmer
import os

class IRSystem(object):
    
    def __init__(self, cmdline_dict, term_selection_reg, term_selection_reg_exclude):
        self.word_reg = term_selection_reg
        self.word_reg_exclude = term_selection_reg_exclude
        self.LOWER_CASE = cmdline_dict['LOWER_CASE']
        self.STEMMING = True
        self.FILTER_STOP_WORDS = cmdline_dict['FILTER_STOP_WORDS']
        self.stop_words_set = set()
        
    def Normalized_words_list(self, document):
        #-----inner function
        def WordListNormalization(document_word_list):
            NeedModification = self.LOWER_CASE or self.STEMMING or self.FILTER_STOP_WORDS
            if NeedModification:
                new_single_word_list = []
                if not self.stop_words_set:
                    stop_list_path = 'stop_list.txt'
                    self.stop_words_set = FilterStopWords.FilterStopWords(stop_list_path)
                for word in document_word_list:
                    if self.LOWER_CASE:
                        word = word.lower()
                    if self.FILTER_STOP_WORDS:
                        dirname=os.path.dirname
                        if word in self.stop_words_set:
                            continue
                    if self.STEMMING:
                        word  = stemming.stemming(word)
                    new_single_word_list.append(word)
                    

                document_word_list = new_single_word_list
            
            return document_word_list

                    
        #--------------------end
        
        #<.><.><.>:::MainCode For FUNCTION Normalized_words_list:::<.><.><.>
        
        # raw sentence_list
        sentence_list = document.lines
        # convert document to bag of words list
        document_in_a_sentence = ''.join(sentence_list)
        document_word_list = Miscellaneous.ConvertStrToBagOfWords(self.word_reg, self.word_reg_exclude, document_in_a_sentence, )
        # normalize every word in document
        normalized_word_list = WordListNormalization(document_word_list)
        # return normalized_word_list
        return normalized_word_list
        #<.><.><.>:::END:::<.><.><.>
