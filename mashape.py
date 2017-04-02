
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



import requests
import os
import sys
import collections
import json
import re



def get_review_file_path_list():
    parent_folder = get_upper_folder_path(2)
    reviews_folder = os.path.join(parent_folder, 'data', 'reviews')
    review_file_name_list = os.listdir(reviews_folder)
    review_file_path_list = []
    for i, review_file in enumerate(review_file_name_list):
        review_file_path = os.path.join(reviews_folder, review_file)
        review_file_path_list.append(review_file_path)
    return review_file_path_list





def get_senti_score(text_content):
    request_dict = {}
    request_dict['language'] = "english"
    request_dict['text'] = text_content
    response = requests.post("https://japerk-text-processing.p.mashape.com/sentiment/",
                             headers={
                                 "X-Mashape-Key": "t2Jx06PDHvmshhIqtaJNG0e8dFotp1QWfSqjsn32LR8ZDwz9mn",
                                 "Content-Type": "application/x-www-form-urlencoded",
                                 "Accept": "application/json"
                             },
                             data=request_dict
                             )

    #print("status_code: ", response.status_code)
    response_dict = response.json()['probability']
    pos_value = response_dict['pos']
    #response_dict['emotion_value'] = response_dict['pos'] - response_dict['neg']

    #print ("response_dict: ", response_dict)
    return pos_value


def get_review_sentiment_dict(review_file_path_list):
    for i, file_path in enumerate(review_file_path_list):
        print("=======================================")
        print ("Analysing {} film!!!!!!!!!!!!".format(i))
        file_date_dict = collections.defaultdict(lambda :[])
        try:
            with open(file_path, 'r', encoding = 'utf-8') as f:
                file_dict = json.load(f)
                for key, value_dict in file_dict.items():
                    print("Analysing {} review...".format(key))
                    date_str = value_dict['date']
                    text_content = value_dict['content']
                    pos_value = float("{:.3f}".format(get_senti_score(text_content)))
                    file_date_dict[date_str].append(pos_value)
        except PermissionError:
            continue
        # get the score
        for date_str, value in file_date_dict.items():
            file_date_dict[date_str] =  float(sum(value) / len(value))



        average_emoion = float("{:.3f}".format(sum(list(file_date_dict.values())) / len(list(file_date_dict.values()))))
        file_date_dict['#average_emoion#'] = average_emoion

        # write to file
        parent_folder = get_upper_folder_path(2)
        #print ("file_path: ", file_path)
        file_name = '[{}]_'.format(average_emoion) + re.findall(r'\\(tt.+?).json', file_path)[0] + '_emotion.json'
        #print ("file_name: ", file_name)
        output_file_name = file_name
        reviews_senti_path = os.path.join(parent_folder, 'data', 'reviews_senti', output_file_name)

        with open(reviews_senti_path, 'w', encoding = 'utf-8') as f:

            json.dump(file_date_dict,f, indent=4)
            print ("write success!")



# main
review_file_path_list = get_review_file_path_list()
get_review_sentiment_dict(review_file_path_list)