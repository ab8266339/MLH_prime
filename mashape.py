
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



def get_review_dicts():
    parent_folder = get_upper_folder_path(2)
    reviews_folder = os.path.join(parent_folder, 'data', 'reviews')
    review_file_name_list = os.listdir(reviews_folder)
    review_file_path_list = []
    for i, review_file in enumerate(review_file_name_list):
        review_file_path = os.path.join(reviews_folder, review_file)
        review_file_path_list.append(review_file_path)



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

    print("status_code: ", response.status_code)
    response_dict = response.json()['probability']
    pos_value = response_dict['pos']
    #response_dict['emotion_value'] = response_dict['pos'] - response_dict['neg']

    print ("response_dict: ", response_dict)
    return pos_value