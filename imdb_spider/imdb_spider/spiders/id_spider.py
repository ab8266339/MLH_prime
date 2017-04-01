from scrapy.contrib.spiders import CrawlSpider
import os
import sys
cuurent_path = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(cuurent_path, 'pjslib')
sys.path.append(lib_path)


from general import get_upper_folder_path

import re



def write_id_to_file(id_list):
    parent_path = get_upper_folder_path(5)
    file_path = os.path.join(parent_path, 'data','imdb_top250_id.txt')
    with open(file_path, 'w', encoding = 'utf-8') as f:
        for id in id_list:
            f.write(id + '\n')




class IdSpider(CrawlSpider):
    name = 'id'
    start_urls = ["http://www.imdb.com/chart/top"]

    def parse(self, response):
        url_list = response.xpath("//td[@class = 'titleColumn']/a").extract()
        imdb_id_list = []
        for url in url_list:
            url = url.encode('utf-8').decode('gbk')
            id = re.findall(r'\/title\/([A-Za-z0-9]+)\/\?', url)[0]
            imdb_id_list.append(id)

        write_id_to_file(imdb_id_list)