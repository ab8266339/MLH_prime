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

from libsvm import *


class MlhSvm():
    def __init__(self):
        self.parent_path = get_upper_folder_path(2)
        self.meta_folder_path = os.path.join(self.parent_path, 'data', 'meta')

        self.review_vector_path = os.path.join(self.parent_path, 'data', 'reviews_vector')


    def read_cls(self):
        meta_file_list = os.listdir(self.meta_folder_path)
        pass
