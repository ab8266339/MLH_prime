import scrapy
from scrapy.contrib.linkextractors.lxmlhtml import  LxmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
import sys
import re
import datetime
import time
import collections
from scrapy.http import Request





# ======================================processing of the crawled data==================================================

def parse_reliability(raw_meta):

    # r_str : 25 out of 27 people found the following revi
    r_str = re.findall(r'<small>([0-9]+) out of ([0-9]+) people found',raw_meta)[0]
    people_trust_num =  int(r_str[0])
    total_num = int(r_str[1])
    reliability_str = "{:.2f}".format(people_trust_num / total_num)
    reliability = float(reliability_str)
    return reliability

def parse_loc(raw_meta):

    try:
        loc = re.findall(r'<small>from ([A-Za-z_, ]+)', raw_meta)[0]
    except IndexError:
        loc = None
    return loc

def parse_review_content(raw_content):
    raw_content = raw_content.replace(r'<p>','')
    raw_content = raw_content.replace(r'</p>', '')
    raw_content = raw_content.replace(r'<\n>', '')
    raw_content = raw_content.strip()
    return raw_content

def parse_time(raw_meta):

    date_str = re.findall(r'<small>([0-9]+ [A-Za-z]+ [0-9]+)', raw_meta)[0]
    date_temp = time.strptime(date_str, '%d %B %Y')
    date = datetime.datetime(*date_temp[:3]).date()

    return date


def write_to_file(review_dict):
    pass



#=======================================================================================================================


class Test2(CrawlSpider):
    name = "test2"
    start_urls = ["http://www.imdb.com/title/tt0092263/reviews?count=92&start=0"]


    def parse(self,response):
        title = response.xpath("//a[@class = 'main']/text()").extract()[0]
        review_dict = collections.defaultdict(lambda: '')
        review_count = 0
        # parse review content==========================================================================================

        review_raw_content_list = response.xpath("//div[@id = 'tn15content']/p").extract()
        #content_test = review_raw_content_list[0].encode('utf-8').decode('gbk')

        for review_content in review_raw_content_list:
            review_dict[review_count] = review_content
            review_count += 1
        # ==============================================================================================================



        # parse meta data===============================================================================================
        review_meta_data_list = response.xpath("//div[@id = 'tn15content']/div").extract()

        for review_meta_data in review_meta_data_list:
            reliability = parse_reliability(review_meta_data)
            loc = parse_loc(review_meta_data)
            date = parse_time(review_meta_data)
            print ("reliability", reliability)
            print("loc", loc)
            print("date", date)
            break
        # ==============================================================================================================




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

