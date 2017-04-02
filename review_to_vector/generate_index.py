def get_upper_folder_path(num, path = ''):
    if not path:
        path = os.path.dirname(os.path.abspath(__file__))
    else:
        path = os.path.dirname(path)
    num -= 1
    if num > 0:
        return get_upper_folder_path(num, path = path)
    else:
        return path


import os
import json
import sys
sys.path.append("read_comments")

from read_documents import ReadDocuments
from ReadWriteIndex import WriteIndexToJson, ReadIndexFromJson
from command_line_input import CommandLine
from inverted_index import InvertedIndex
from miscellaneous import Miscellaneous


def temp_write(data, name = "temp"):
    path = os.path.join(os.path.dirname(__file__), "test_output/{}.txt".format(name))
    with open (path, 'w', encoding = 'utf-8') as f:
        for doc in data:
            f.write(doc.docid)
            f.write('\n')
            f.write(doc.date)
            f.write('\n')
            f.write(str(doc.lines))
            f.write('\n')

def get_tf_idf_parameters(parameter_file_name = 'tfidf_parameters'):
    # parameter_input_folder: input_parameters(fixed)
    current_path = Miscellaneous.find_upper_level_folder_path(1)
    parameter_file_name_path = os.path.join(current_path, 'input_parameters', parameter_file_name + '.json')
    with open(parameter_file_name_path, 'r', encoding = 'utf-8') as f:
        tfidf_parameter_dict = json.load(f)
    return tfidf_parameter_dict


    
    
# ------------main start----------------
if __name__ == "__main__":
    # get all the parameters
    parent_folder = get_upper_folder_path(3)



    inverted_index_name = 'imdb250_idf.json'
    inverted_index_path = os.path.join(parent_folder, 'data', inverted_index_name)

    #--------------------------
    cmdline_dict= CommandLine.CommandLineInputInfo()
    #inverted_index_path = CommandLine.CreateCommandLinePath(inverted_index_path_prefix, cmdline_dict)


    # (2) create inverted_index and detect whether the inverted index has already been created based on path name
    term_selection_reg_exclude = r''
    term_selection_reg_exclude = r'^$'
    term_selection_reg = r'([\w\d]+)'
    invertedindex = InvertedIndex(cmdline_dict, term_selection_reg,term_selection_reg_exclude)
    file_folder_path = os.path.join(parent_folder, 'data', 'reviews')

    corpus = ReadDocuments(file_folder_path)

    # for corpus1 in corpus:
    #     print (corpus1.docid)
    #     print(corpus1.lines)
    #     break

    # (3) create new inverted_index
    inverted_index_dict = invertedindex.CreateInvertedIndexFromDocumentCollection(corpus)

    print("---------------------------------------------")
    print("Writing new inverted_index...")
    print ('inverted_index_path--------- ', inverted_index_path)
    WriteIndexToJson(inverted_index_dict, inverted_index_path)
    print("Writing new inverted_index completed!")