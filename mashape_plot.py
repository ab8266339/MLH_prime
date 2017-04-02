
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



import matplotlib.pyplot as plt
import os
import re
import sys
import collections


parent_folder = get_upper_folder_path(2)
senti_folder = os.path.join(parent_folder, 'data', 'reviews_senti')
senti_file_list = os.listdir(senti_folder)
senti_file_list = [os.path.join(senti_folder, x) for x in senti_file_list]

meta_folder_path = os.path.join(parent_folder, 'data', 'meta')
meta_file_list = os.listdir(meta_folder_path)
id_name_dict = collections.defaultdict(lambda :[0,0,0,0])

def plot_emotion_trend():
    for senti_file in senti_file_list:
        with open(senti_file, 'r') as f:
            f.write()






def get_movie_rating_vs_emotion():
    r_vs_emo_dict = collections.defaultdict(lambda :[0,0,0,0])
    for file in senti_file_list:
        with open(file, 'r') as f:
            emotion_score = re.findall(r'\[([0-9.]+)\]', f.name)[0]
            id = re.findall(r'\]_(tt[0-9]+)_', f.name)[0]
            for meta_file in meta_file_list:
                is_id_found = re.findall(id, meta_file)
                if is_id_found:
                    rank = re.findall(r'^([0-9]+)', meta_file)[0]
                    rating = re.findall(r'^[0-9]+_([0-9.]+)_', meta_file)[0]
                    name = re.findall(r'\[r\][0-9]+_(.*?)_meta.json', meta_file)[0]
                    break

            r_vs_emo_dict[id][0] = emotion_score
            r_vs_emo_dict[id][2] = rating
            r_vs_emo_dict[id][3] = rank
            id_name_dict[id] = name


    # get the emotion rank
    r_vs_emo_list = sorted(list(r_vs_emo_dict.items()), key = lambda x:x[1][0], reverse = True)
    r_vs_emo_new_list = r_vs_emo_list.copy()
    print ("r_vs_emo_list: ", r_vs_emo_list)
    for i, value_list in enumerate(r_vs_emo_list):
        #  r_vs_emo_list: [['0.806', 0, '8.5', '155'], ['0.67', 0, '8.3', '203']]
        id = value_list[0]
        emotion_score = value_list[1][0]
        #emotion_rank = value_list[1]
        rating_score = value_list[1][2]
        rating_rank = value_list[1][3]
        r_vs_emo_new_list[i] = [emotion_score, str(i), rating_score, rating_rank, id]


    # write to file
    output_r_vs_emo_path = os.path.join(parent_folder, 'data', 'r_vs_emo.txt')
    with open(output_r_vs_emo_path, 'w', encoding = 'utf-8') as f:
        for list1 in r_vs_emo_new_list:
            print ("r_vs_emo_new_list: ", r_vs_emo_new_list)
            f.write(str(list1[0]) + ',')
            f.write(str(list1[1]) + ',')
            f.write(str(list1[2]) + ',')
            f.write(str(list1[3]) +  ',')
            id = list1[4]
            name = id_name_dict[id]
            f.write(str(list1[4]) + ',')
            print ("name: ", name)
            f.write(name + '\n')



# main

get_movie_rating_vs_emotion()