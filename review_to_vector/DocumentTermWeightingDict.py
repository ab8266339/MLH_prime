import collections
import os
import numpy as np
from ReadWriteIndex import WriteIndexToJson, ReadIndexFromJson

class DocumentTermWeightingDict():
    def __init__(self, inverted_index_dict, cmdline_dict):
        self.inverted_index_dict = inverted_index_dict
        
        self.cmdline_dict = cmdline_dict
        self.basic_path = "document_term_weighting_json_file"
        # minor modification
        self.weighting = cmdline_dict['mode']
        if cmdline_dict['mode'] == "tfidf":
            self.weighting = "tf_idf"
        elif cmdline_dict['mode'] == "term_frequency":
            self.weighting = "tf"

    def CreatePath(self):
        path = self.basic_path
        if self.cmdline_dict['STEMMING']:
            path = path + '+STEMMING'
        if self.cmdline_dict['FILTER_STOP_WORDS']:
            path = path + '+FILTER_STOP_WORDS'
        if self.cmdline_dict['mode']:
            path = path + '+' + self.cmdline_dict['mode']
        path = path + '.txt'
        return path
    
    def NormalizeSum(self, term_weighting_dict):
        #{"187": {"term_weighting_dict": {"june": 1.0300213190877703, "connectives": 3.2046625117482184, "compiling": 2.1834732126782805,...}
        for doc in term_weighting_dict:
            value_list = list(term_weighting_dict[doc]['term_weighting_dict'].values())
            value_array = np.asarray(value_list)
            #print ("value_list", value_list)
            normalize_sum = (np.sum(value_array**2))**0.5
            term_weighting_dict[doc]['normalize_sum'] = normalize_sum
        return term_weighting_dict
    
    def CreateDocumentTermWeightingDict(self):
        term_weighting_dict = collections.defaultdict(lambda: {'weighting':self.weighting, 'normalize_sum':0, 'term_weighting_dict': collections.defaultdict(lambda:0)})
        
        for word in self.inverted_index_dict:
        ##{"dayhoff": {"idf": 3.5056925074122, "documents_dict": {"699": {"tf": 1, "tf_idf": 3.5056925074122}}, "df": 1}}
            document_list = list(self.inverted_index_dict[word]["documents_dict"])
            for document in document_list:
                document = str(document)
                if self.weighting == "binary":
                    term_weighting_dict[document]['term_weighting_dict'][word] = 1
                else:
                    term_weighting_dict[document]['term_weighting_dict'][word] = self.inverted_index_dict[word]["documents_dict"][document][self.weighting]
                    
        term_weighting_dict = self.NormalizeSum(term_weighting_dict)
        return term_weighting_dict
        
    def CreateDocumentTermWeightingMain(self):
        # (1.1) detect path
        path = self.CreatePath()
        if path in os.listdir():
            term_weighting_dict = ReadIndexFromJson(path)
            return term_weighting_dict
        # (1.2)if document is not in the path, create new one and write
        else:
            term_weighting_dict = self.CreateDocumentTermWeightingDict()
            WriteIndexToJson(term_weighting_dict, path)
            return term_weighting_dict
        
        
        
        
        