import scrapy
from scrapy.contrib.linkextractors.lxmlhtml import  LxmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
import sys
import re
import datetime
import time
import os
import collections
import json

cuurent_path = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(cuurent_path, 'pjslib')
sys.path.append(lib_path)

from logger import logger1
from general import get_upper_folder_path
from scrapy.http import Request





# ======================================processing of the crawled data==================================================

def get_is_valid_div(raw_meta):
    r_str = re.findall(r'\<b\>Author', raw_meta)
    if not r_str:
        return False
    else:
        return True


def parse_reliability(raw_meta):

    # r_str : 25 out of 27 people found the following revi
    #print("--------------")
    try:
        r_str = re.findall(r'<small>([0-9]+) out of ([0-9]+) people found',raw_meta)[0]
        people_trust_num = int(r_str[0])
        total_num = int(r_str[1])
        reliability_str = "{:.2f}".format(people_trust_num / total_num)
        reliability = float(reliability_str)

    except IndexError:
        reliability = 0
    return reliability

#{'tt0087544', 'tt0056687', 'tt0056801'}

def parse_loc(raw_meta):

    try:
        loc = re.findall(r'<small>from ([A-Za-z_, ]+)', raw_meta)[0]
    except IndexError:
        loc = None
    return loc

def parse_review_content(raw_content):
    raw_content = re.subn(r'(<[A-Za-z0-9\/]+>)', '', raw_content)[0]
    raw_content = re.subn(r'[^A-Za-z0-9\-\(\)\'\"\.\,\!\?\;\:]+', ' ', raw_content)[0]
    raw_content = raw_content.strip()
    return raw_content

def parse_time(raw_meta):

    date_str = re.findall(r'<small>([0-9]+ [A-Za-z]+ [0-9]+)', raw_meta)[0]
    date_temp = time.strptime(date_str, '%d %B %Y')
    date = datetime.datetime(*date_temp[:3]).date()

    return date


def write_to_file(review_dict, file_name):
    parent_path = get_upper_folder_path(5)
    file_path = os.path.join(parent_path, 'data', 'reviews', file_name)
    with open (file_path, 'w', encoding = 'utf-8') as f:
        json.dump(review_dict, f, indent = 4)


def read_start_url():
    parent_path = get_upper_folder_path(5)
    file_name = 'imdb_top250_id.txt'
    file_path = os.path.join(parent_path, 'data', file_name)
    meta_folder = os.path.join(parent_path, 'data', 'meta')
    meta_file_list = os.listdir(meta_folder)
    start_urls = []
    for file_name in meta_file_list:
        #print ("file_name", file_name)
        id = re.findall(r'_(tt[0-9]+)_', file_name)[0]
        review_count = re.findall(r'_\[r\]([0-9]+)_', file_name)[0]
        url = "http://www.imdb.com/title/{}/reviews?count={}&start=0".format(id, review_count)
        start_urls.append(url)

    return start_urls

#=======================================================================================================================


class Imdb_Review_Spider(CrawlSpider):
    name = "review"
    start_urls_temp = read_start_url()

    #start_urls = start_urls_temp
    start_urls = ['http://www.imdb.com/title/tt0087544/reviews?count=187&start=0']
    print ("start_urls: ", start_urls)

    def parse(self,response):
        title = response.xpath("//a[@class = 'main']/text()").extract()[0]
        title = title.replace(r':','-')
        title = title.replace(r'<', '')
        title = title.replace(r'>', '')
        title = title.replace(r'>', '')
        title = title.replace(r'"', '')
        title = title.replace(r'\/', '')
        title = title.replace(r'\\', '')
        title = title.replace(r'\|', '')
        title = title.replace(r'?', '')
        title = title.replace(r'*', '')
        #print ("title: ", title)
        review_dict = collections.defaultdict(lambda: collections.defaultdict(lambda:0))
        review_count = 0
        # parse review content and meta=================================================================================

        # content
        review_raw_content_list = response.xpath("//div[@id = 'tn15content']/p").extract()
        # meta
        review_meta_data_list = response.xpath("//div[@id = 'tn15content']/div").extract()
        #content_test = review_raw_content_list[0].encode('utf-8').decode('gbk')

        # ==============================================================================================================


        # get the file name
        url = response.url
        # url: http://www.imdb.com/title/tt0092263/reviews?count=92&start=0
        file_name = re.findall(r'title\/([A-Za-z0-9]+)', url)[0]
        file_name = file_name + '_' + title + '_review' + '.json'
        #
        # filter the invalid div
        filtered_review_meta_data_list = []
        for review_meta_data in review_meta_data_list:
            is_valid_div = get_is_valid_div(review_meta_data)
            if is_valid_div:
                filtered_review_meta_data_list.append(review_meta_data)


        print ("filtered_review_meta_data_list_len: ", len(filtered_review_meta_data_list))
        print("review_raw_content_list: ", len(review_raw_content_list))

        for review_meta_data, raw_review_content in zip(filtered_review_meta_data_list, review_raw_content_list):

            review_content = parse_review_content(raw_review_content)
            review_dict[review_count]['content'] = review_content
            reliability = parse_reliability(review_meta_data)
            loc = parse_loc(review_meta_data)
            date = parse_time(review_meta_data)
            # convert date to date_str
            date_str = date.strftime("%Y-%m-%d")
            review_dict[review_count]['reliability'] = reliability
            review_dict[review_count]['loc'] = loc
            review_dict[review_count]['date'] = date_str
            review_count += 1
            # print ("reliability", reliability)
            # print("loc", loc)
            # print("date", date)
        # ==============================================================================================================

        write_to_file(review_dict, file_name)



        # review_meta_data_len = len(review_meta_data)
        # meta_data_num = 3

        # # get the raw data
        # raw_review_reliability_list = review_meta_data[0:review_meta_data_len:meta_data_num]
        # raw_review_loc = review_meta_data[1:review_meta_data_len:meta_data_num]
        # raw_review_time = review_meta_data[2:review_meta_data_len:meta_data_num]
        #
        # # process the data
        # review_loc = parse_loc(raw_review_loc)
        # review_time = parse_time(raw_review_time)
        # # print("review_reliability_list: ", review_reliability_list)
        # # print("review_loc: ", review_loc)
        # # print ("review_time: ", review_time)
        #
        # #print("review_reliability_list[0]: ", review_reliability_list[0])
        # print("review_loc[0]: ", review_loc[0])
        # print ("review_time[0]: ", review_time[0])

