import collections
import re
import sys
import math
import os
import nltk
import numpy as np
from read_documents import ReadDocuments
from ReadWriteIndex import WriteIndexToJson, ReadIndexFromJson
from irsystem import IRSystem
from logger import logger1


class InvertedIndex(IRSystem):
    
    def __init__(self, cmdline_dict, term_selection_reg, term_selection_reg_exclude):
        super().__init__(cmdline_dict, term_selection_reg, term_selection_reg_exclude)
        self.D = 0 
        self.documents_obj_list = []
        self.is_MLH_PRIME = True
        if not self.is_MLH_PRIME:
            self.inverted_index_dict = collections.defaultdict(lambda: {'df':0, 'idf':0, 'documents_dict':collections.defaultdict(lambda: {'tf':0, 'tf_idf':0})})
        else:
            self.inverted_index_dict = collections.defaultdict(
                lambda: {'df': 0, 'idf': 0})
    def ComputeDfTf(self, document_id, normalized_word_list):
        id = document_id
        #TODO could be a json bug
        id = str(id)
        # one document, one document_word_set
        document_word_set = set()
        for word in normalized_word_list:
            if not (word in document_word_set):
                document_word_set.add(word)
                #compute df of each unduplicated word in the document
                self.inverted_index_dict[word]['df'] += 1
            #compute tf of each word in the document
            if not self.is_MLH_PRIME:
                self.inverted_index_dict[word]['documents_dict'][id]['tf'] += 1
            
    def ComputeIdf(self):
        log_base_num = 10
        for word in self.inverted_index_dict.keys():
            self.inverted_index_dict[word]['idf'] = math.log(self.D / self.inverted_index_dict[word]['df'], log_base_num)
            
    def ComputeTfIdf(self):
        log_base_num = 10
        for word in self.inverted_index_dict.keys():
            #fetch idf of every word
            word_idf = self.inverted_index_dict[word]['idf']
            #compute tf.idf for every word in this document
            for key, document in self.inverted_index_dict[word]['documents_dict'].items():
                #print (document)
                #sys.exit()
                document['tf_idf'] = document['tf'] * word_idf
    
    def CreateInvertedIndexFromDocumentCollection(self, document_collection):
        # for each document in document collection
        # document_collection consists of single document objects
        
        #normalize word and compute df, tf
        print("creating Inverted Index...")
        for doc in document_collection:
            print ("doc_id: {}".format(doc.docid))
            # doc.docid = 0; doc.lines = []
            # logger1.info("id:{}".format(doc.docid))
            self.D = self.D + 1
            # (1) normalized_words_list
            normalized_words_list = self.Normalized_words_list(doc)
            
            # (2) get id and compute df, tf
            document_id = doc.docid
            self.ComputeDfTf(document_id, normalized_words_list)
        # (3) compute idf of words
        self.ComputeIdf()
        # (4) compute tf_idf
        if not self.is_MLH_PRIME:
            self.ComputeTfIdf()
        print("creating Inverted Index Complete...")
        # (5) return
        return self.inverted_index_dict

    
    
    