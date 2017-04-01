from scrapy.contrib.spiders import CrawlSpider
import os
from pjslib.general import get_upper_folder_path

import re
import json
import re


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
    start_urls = [url_list[0]]

    def parse(self, response):
        url = response.url
        id = re.findall(r'title\/([A-Za-z0-9]+)', url)[0]

        # (1.) file_name
        film_name = response.xpath("//h1[@itemprop = 'name']/text()").extract()[0]
        film_name = re.subn(r'[^A-Za-z\-0-9 \:]+', '', film_name)[0]

        # (2.) rating
        rating = response.xpath("//span[@itemprop = 'ratingValue']/text()").extract()[0]
        rating = float(rating)

        # (3.) rating num
        rating_count = response.xpath("//span[@itemprop = 'ratingCount']/text()").extract()[0]
        rating_count = rating_count.replace(r',','')
        rating_count = int(rating_count)

        # (4.) director
        director = response.xpath("//span[@itemprop = 'director']/a/span/text()").extract()[0]


        # print
        print("film_name: ", film_name)
        print ("rating: ", rating)
        print("rating_count: ", rating_count)
        print("director: ", director)
