from scrapy.contrib.spiders import CrawlSpider
import os


import re
import sys
import json
import re
import collections
from bs4 import BeautifulSoup
sys.path.append('pjslib')
from general import get_upper_folder_path

from lxml.html.clean import clean_html


def write_id_to_file(id_list):
    parent_path = get_upper_folder_path(5)
    file_path = os.path.join(parent_path, 'data','imdb_top250_id.txt')
    with open(file_path, 'w', encoding = 'utf-8') as f:
        for id in id_list:
            f.write(id + '\n')

def read_start_ids(path):
    id_list = []
    with open (path, 'r', encoding = 'utf-8') as f:
        for line in f:
            id_list.append(line.strip())
    return id_list

def convert_id_list_to_url_list(id_list):
    url_list = []
    for id in id_list:
        url = "http://www.imdb.com/title/{}/".format(id)
        url_list.append(url)

    return url_list


def write_meta_data(meta_dict, file_name):
    parent_path = get_upper_folder_path(5)
    file_path = os.path.join(parent_path, 'data', 'meta', file_name)
    with open (file_path, 'w', encoding = 'utf-8') as f:
        json.dump(meta_dict, f, indent=4)



class IdSpider(CrawlSpider):
    name = 'meta'
    parent_path = get_upper_folder_path(5)
    imdb_250_file_path = os.path.join(parent_path, 'data', 'imdb_top250_id.txt')
    id_list = read_start_ids(imdb_250_file_path)
    url_list = convert_id_list_to_url_list(id_list)
    #start_urls = [url_list[-1]]
    start_urls = url_list

    def parse(self, response):
        url = response.url
        id = re.findall(r'title\/([A-Za-z0-9]+)', url)[0]

        # (0.) rank
        try:
            rank_srt = response.xpath("//a[@href = '/chart/top?ref_=tt_awd']/text()").extract()[0]
            rank = re.findall(r'[0-9]+', rank_srt)[0]
        except IndexError:
            rank = '250'


        # (1.) file_name
        film_name = response.xpath("//h1[@itemprop = 'name']/text()").extract()[0]
        film_name = re.subn(r'[^A-Za-z\-0-9 \:]', '', film_name)[0]
        film_name = film_name.replace(':','-')

        print ("film_name: ", film_name)

        # (2.) rating
        rating = response.xpath("//span[@itemprop = 'ratingValue']/text()").extract()[0]
        rating = float(rating)

        # (3.) rating num
        rating_count = response.xpath("//span[@itemprop = 'ratingCount']/text()").extract()[0]
        rating_count = rating_count.replace(r',','')
        rating_count = int(rating_count)

        # (4.) director
        director = response.xpath("//span[@itemprop = 'director']/a/span/text()").extract()[0]

        # (5.) writer
        writer = response.xpath(
            "//div[@class = 'credit_summary_item']//span[@itemprop = 'creator']/a/span/text()").extract()

        # (6.) stars
        stars = response.xpath(
            "//span[@itemprop = 'actors']/a/span[@itemprop = 'name']/text()").extract()

        # (7.) reviews_count
        reviews_count = response.xpath(
            "//a[@href = 'reviews?ref_=tt_ov_rt']/text()").extract()[0]
        reviews_count = reviews_count.replace(r',','')
        reviews_count = re.findall(r'[0-9]+',reviews_count)[0]

        # (8.) Genres
        genres = response.xpath(
            "//div[@itemprop = 'genre']//a/text()").extract()
        genres = [x.strip() for x in genres]

        # (9) title detial
        titleDetails = response.xpath(
            "//div[@id='titleDetails']").extract()[0]
        #titleDetails = titleDetails.encode('utf-8').decode('gbk')

        VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br']

        def sanitize_html(value):
            soup = BeautifulSoup(value, 'lxml')
            for tag in soup.findAll(True):
                if tag.name not in VALID_TAGS:
                    tag.hidden = True
            return soup.renderContents()

        titleDetails = sanitize_html(titleDetails).decode('utf-8')
        titleDetails = titleDetails.replace('\n','')


        # country
        try:
            country = re.findall(r'Country:(.+?)Language',titleDetails)[0]
        except IndexError:
            country = None

        # language
        try:
            language = re.findall(r'Language:(.+?)Release',titleDetails)[0]
        except IndexError:
            language = None
        # filming_loc
        try:
            filming_loc = re.findall(r'Filming Locations:(.+?)See more',titleDetails)[0]
        except IndexError:
            filming_loc = None

        # budget
        try:
            budget = re.findall(r'OfficeBudget:.*?([0-9\,]+).*Gross',titleDetails)[0]
            budget = budget.replace(r',', '')
        except IndexError:
            budget = None

        # gross
        try:
            gross = re.findall(r'Gross:.*?([0-9\,]+).*See more',titleDetails)[0]
            gross = gross.replace(r',', '')
        except IndexError:
            gross = None


        # run_time
        try:
            run_time = re.findall(r'Runtime:.*?([0-9]+).*min',titleDetails)[0]
            run_time = run_time.replace(r',', '')
        except IndexError:
            run_time = None




        # save_meta_dict
        meta_dict = collections.defaultdict(lambda :0)
        meta_dict['id'] = id
        meta_dict['rank'] = rank
        meta_dict['film_name'] = film_name
        meta_dict['rating'] = rating
        meta_dict['rating_count'] = rating_count
        meta_dict['director'] = director
        meta_dict['writer'] = writer
        meta_dict['stars'] = stars
        meta_dict['reviews_count'] = reviews_count
        meta_dict['genres'] = genres
        meta_dict['language'] = language
        meta_dict['country'] = country
        meta_dict['filming_loc'] = filming_loc
        meta_dict['budget'] = budget
        meta_dict['gross'] = gross
        meta_dict['run_time'] = run_time

        # print ("country: ",country)
        # print ("filming_loc: ", filming_loc)
        # meta_file_name
        meta_file_name = rank + '_' + str(id) + '_' + film_name + '_meta.json'
        write_meta_data(meta_dict, meta_file_name)


        # print




