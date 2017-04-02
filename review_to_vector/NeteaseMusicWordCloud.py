import os,sys
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
from miscellaneous import Miscellaneous
from read_comments.read_comments import ReadDocuments
from command_line_input import CommandLine
from irsystem import IRSystem
import jieba
import collections
import json
import random





class NeteaseWordCloud(IRSystem):
    #def __init__(self, cmdline_dict, singer = '', song_id = '', output_file_name = '', mask_pic = ''):
    def __init__(self, cmdline_dict, parameter_file_name = 'NeteaseMusicWordCloud_parameters'):

        def get_input_parameters_dict(parameter_file_name):
            parameter_file_path = os.path.join(self.current_path, 'input_parameters', parameter_file_name + '.json')
            with open(parameter_file_path, 'r', encoding = 'utf-8') as f:
                self.input_parameters_dict = json.load(f)
            return self.input_parameters_dict
            
            
        def get_output_path(singer, song_id, output_file_name):
            # #pass
            input = Miscellaneous.singer_or_id(singer, song_id)
            if not input:
                #TODO cmd
                sys.exit(0)
            if input == 'singer':
                self.SINGER_MODE = True
                self.ID_MODE  = False
            elif input == 'id':
                self.SINGER_MODE = False
                self.ID_MODE  = True
            #create default output_path
            # print ("output_file_name: ", output_file_name)
            if not output_file_name:
                output_file_name = song_id + singer 
            output_path = Miscellaneous.find_upper_level_folder_path(1)
            output_path = os.path.join(output_path, 'output', output_file_name + '.json')
            return output_path
            
        def get_input_path(singer, song_id, output_file_name):
            input_path = ''
            if self.SINGER_MODE:
                input_path = Miscellaneous.find_upper_level_folder_path(3)
                input_path = os.path.join(input_path, 'music_database')
                input_path = os.path.join(input_path, singer)
                self.singer_name = singer
            elif self.ID_MODE:
                input_path = Miscellaneous.find_upper_level_folder_path(3)
                input_path = os.path.join(input_path, 'music_database')
                singer = Miscellaneous.find_singer(song_id)
                input_path = os.path.join(input_path, singer)
                input_path = os.path.join(input_path, song_id + '.json')
            return input_path
        
        #<MAIN>----------------------------------------:::__init__:::----------------------------------------<MAIN>
        super().__init__(cmdline_dict)
        self.current_path = Miscellaneous.find_upper_level_folder_path(1)
        #----------------------read parameters
        self.parameter_file_name = parameter_file_name
        # default and fixed parameter folder: input_parameters
        # parameter_file shoule be json(eg. NeteaseMusicWordCloud_parameters.json)
        input_parameters_dict = get_input_parameters_dict(self.parameter_file_name)
        # singer = '', song_id = '', output_file_name = '', mask_pic = ''
        singer = input_parameters_dict['general']['singer']
        song_id = input_parameters_dict['general']['song_id']
        output_file_name = input_parameters_dict['general']['output_file_name']
        mask_pic = input_parameters_dict['general']['mask_pic']
        # set different paths
        self.mask_pic = mask_pic
        if self.mask_pic:
            mask_pictures_set = set(os.listdir(os.path.join(Miscellaneous.find_upper_level_folder_path(1), 'mask_pictures')))
            if (not self.mask_pic in mask_pictures_set):
                print ("mask_picture doesn't exists!")
                #TODO
                sys.exit(0)
            else:
                self.mask_pic_path = os.path.join(os.path.join(Miscellaneous.find_upper_level_folder_path(1), 'mask_pictures', self.mask_pic))
            self.MASK_PIC = True
        else:
            self.MASK_PIC = False
        self.output_path = get_output_path(singer, song_id, output_file_name)
        # remove .json for image
        self.output_image_path =  self.output_path[:len(self.output_path) - 5] + '_image' + '.png'
        print ("self.output_image_path: ", self.output_image_path)
        self.output_sorted_dict_path =  self.output_path[:len(self.output_path) - 5] + '_sorted' + '.txt'
        self.inputpath = get_input_path(singer, song_id, output_file_name)
        # get inverted_index 
        current_path = Miscellaneous.find_upper_level_folder_path(1)
        inverted_index_path = os.path.join(current_path, "inverted_index", "NeteaseMusic_inverted_index.json")
        with open(inverted_index_path, encoding = 'utf-8') as f:
            self.inverted_index = json.load(f)
        #print("inputpath", self.inputpath)
        #print("output_path", self.output_path)
        
        

        

        
    def write_tfidf_dict(self):
        print ("self.output_path: ", self.output_path)
        with open(self.output_path, 'w', encoding = 'utf-8') as f:
            json.dump(self.cleaned_tf_idf_dict, f, ensure_ascii=False, indent = 4)
            
    def get_cleaned_tfidf_dict(self):
    
        def get_documents():
            if self.ID_MODE:
                filepath = self.inputpath
                #print ("filepath: ",filepath)
                corpus = ReadDocuments(single_file_path = filepath)
                for doc in corpus:
                    print ("docid: ", doc.docid)
            elif self.SINGER_MODE:
                singer_name = self.singer_name
                corpus = ReadDocuments(singer_name = singer_name)
                for doc in corpus:
                    print ("docid: ", doc.docid)
            self.document_collection = corpus
            
        def get_tf_dict(words_list):
            # get tf_dict
            cleaned_dict = collections.defaultdict(lambda:0)
            for word in words_list:
                cleaned_dict[word] += 1
            return cleaned_dict
        # get cleaned word lists
        
        #....................::get_cleaned_tfidf_dict::...........................
        # get input document_collection (may include many docs)
        get_documents()
        
        whole_words_list = []
        for doc in self.document_collection:
            normalized_words_list = self.Normalized_words_list(doc)
            whole_words_list.extend(normalized_words_list)
        # get tf_dict
        cleaned_dict = get_tf_dict(whole_words_list)
        # get tf_idf dict
        for key, value in cleaned_dict.items():
            word_idf = self.inverted_index[key]['idf']
            cleaned_dict[key] = value * word_idf
        self.cleaned_tf_idf_dict = cleaned_dict
            
    def display_and_output_word_cloud(self):
    
        def get_word_cloud_list():
            word_cloud_list = self.cleaned_tf_idf_dict.items()
            return word_cloud_list
        
        def initialize_and_display(mask_pic_path, parameter_dict, word_cloud_list):
            # initialize parameters
            margin = parameter_dict['margin']
            font_path = parameter_dict['font_path']
            width = parameter_dict['width']
            height = parameter_dict['height']
            max_font_size = parameter_dict['max_font_size']
            background_color = parameter_dict['background_color']
            max_words = parameter_dict['max_words']
            scale = parameter_dict['scale']
            #mask
            if mask_pic_path:
                mask_pic = np.array(Image.open(mask_pic_path))
                wordcloud = WordCloud(font_path = font_path,margin = margin, width = width, max_font_size = max_font_size, height = height, background_color = background_color, max_words = max_words, mask=mask_pic, scale = scale)
                wordcloud.generate_from_frequencies(word_cloud_list)
                image_colors = ImageColorGenerator(mask_pic)
                plt.title("Mask")
                plt.imshow(wordcloud.recolor(color_func=image_colors))
                plt.show()
            #normal
            if not mask_pic_path:
                wordcloud = WordCloud(font_path = font_path,margin = margin, width = width, max_font_size = max_font_size, height = height, background_color = background_color, max_words = max_words, scale = scale)
                wordcloud.generate_from_frequencies(word_cloud_list)
                plt.title("Normal")
                plt.imshow(wordcloud)
                plt.show()
            return wordcloud

        def save_file_image(wordcloud):
            # write sorted wordcloud_dict
            with open(self.output_sorted_dict_path, 'w', encoding = 'utf-8') as f:
                tuple_list = sorted(self.cleaned_tf_idf_dict.items(), key = lambda x:x[1], reverse = True)
                # add \n to every element
                tuple_list = list(map(lambda x:str(x)+'\n',tuple_list))
                wordcloud_string = ''.join(tuple_list)
                f.write(wordcloud_string)
            # save image
            wordcloud.to_file(self.output_image_path)
            
        
        #....................::display_and_output_word_cloud::...........................
        # mask_pic_path
        if self.MASK_PIC:
            mask_pic_path = self.mask_pic_path
        else:
            mask_pic_path = ''
        # word_cloud_list
        word_cloud_list = get_word_cloud_list()
        # parameter_dict
        parameter_dict = self.input_parameters_dict['wordcloud']

        wordcloud = initialize_and_display(mask_pic_path, parameter_dict, word_cloud_list)
        save_file_image(wordcloud)
            
            
        

#command_line
cmdline_dict= CommandLine.CommandLineInputInfo()
word_cloud = NeteaseWordCloud(cmdline_dict)
# get tfidf_dict for chosen song or folder
word_cloud.get_cleaned_tfidf_dict()
# write tf_idf json for chosen song or folder
word_cloud.write_tfidf_dict()
word_cloud.display_and_output_word_cloud()
#word_cloud = NeteaseWordCloud(song_id = '2638a1196')