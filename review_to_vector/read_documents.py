
import re, sys
import os
import json
import datetime

class ReadDocuments:
    #TODO create a function that can use len()
    def __init__(self,file_folder_path):
        self.file_folder_path = file_folder_path

    def __iter__(self):
        file_path_list = os.listdir(self.file_folder_path)
        for file_path in file_path_list:
            file_path = os.path.join(self.file_folder_path, file_path)
            try:
                film_id = re.findall(r'(tt[0-9]+)_', file_path)[0]
            except IndexError:
                continue
            with open(file_path, 'r', encoding = 'utf-8') as f:
                reviews_dict = json.load(f)
                # review_dict
                # "date": "2003-01-13",
                # "reliability": 0.85,
                # "content": "asdsadsad sadasd"
                # "loc": "Finland"
                for key, review_dict in reviews_dict.items():
                    doc = Document()
                    doc.docid = film_id + '_' + str(key)
                    doc.date = review_dict['date']
                    doc.lines = review_dict['content'].split('.')
                    doc.loc = review_dict['loc']
                    yield doc





class Document:
    def __init__(self):
        self.docid = 0
        self.date = ''
        self.loc = ''
        self.lines = []

    def printDoc(self):

        for line in self.lines:
            print(line, end='')

