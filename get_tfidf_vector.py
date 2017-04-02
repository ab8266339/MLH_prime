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
import sys
import json
import re
import collections
from nltk.stem import PorterStemmer

# ==========================
def filter_words_list(word_list):
    new_word_list = []
    is_stemming = True


    # filter stopwords
    stop_list_path = './review_to_vector/stop_list.txt'
    with open(stop_list_path, 'r') as f:
        stop_words_list = f.readlines()

    stop_words_set = set(stop_words_list)
    for word in word_list:
        if word in stop_words_set:
            pass
        else:
            new_word_list.append(word)
    #

    # stemming
    if is_stemming:
        stemmer = PorterStemmer()
        for i, word in enumerate(new_word_list):
            word = stemmer.stem(word)
            new_word_list[i] = word
    #
    return new_word_list

def write_movie_vector(movie_word_tfidf_dict, review_vector_path):
    #　csv
    with open (review_vector_path, 'w', encoding = 'utf-8') as f:
        for word, tf_idf in movie_word_tfidf_dict.items():
            f.write(word + )
    pass

#=======================================================================================================================


# get tfidf-idf
parent_path = get_upper_folder_path(2)
idf_file_name = 'imdb250_idf.json'
idf_file_path = os.path.join(parent_path, 'data', idf_file_name)

with open (idf_file_path, 'r', encoding = 'utf-8') as f:
    idf_dict = json.load(f)



# get word_frequency for each article
review_folder_path = os.path.join(parent_path, 'data', 'reviews')
review_file_name_list = os.listdir(review_folder_path)

for review_file_path in review_file_name_list:
    review_vector_path = review_file_path.replace('review','vector')
    with open (review_file_path, 'r', encoding = 'utf-8') as f:
        movie_word_f_dict = collections.defaultdict(lambda :0)
        movie_word_tfidf_dict = collections.defaultdict(lambda :0)
        reviews_file_dict = json.load(f)
        for key, review_dict in reviews_file_dict.items():
            content = review_dict['content']
            words_list = re.findall('([\w\d]+)', content)
            new_words_list = filter_words_list(words_list)

            # get frequency
            for word in new_words_list:
                movie_word_f_dict[word] += 1

        # get tf_idf
        for word_f, value in movie_word_f_dict.items():
            is_word_in_idf = idf_dict.get(word_f)
            if is_word_in_idf:
                tf_value = word_f
                idf_value = idf_dict[word_f]['idf']
                movie_word_tfidf_dict[word_f] = tf_value * idf_value
            else:
                movie_word_tfidf_dict[word_f] = 0



















