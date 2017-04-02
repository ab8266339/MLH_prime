import numpy as np

class ComputeCosSimilarity(object):
    
    def __init__(self):
        pass
    # normalized array of doc1, doc2, matrix nx1
    @staticmethod
    def NormarlizeMatrix(matrix):
        return matrix
    @staticmethod
    def NormarlizeArray(array):
        sum_square = 0
        for value in array:
            sum_square += value**2
        sum_square_root = sum_square ** 0.5
        array = array / sum_square_root
        return array
    
    @staticmethod
    def CosThetaBetweenArray(array1, array2):
        cos_theta = np.dot(array1, array2)
        return cos_theta
    # return K nearest documents(id) with respect to query
    @staticmethod
    def CosSimilarDocuments(query, inverted_index_dic, k = None):
        pass
    @staticmethod
    # array1 and array2 are not normalized
    def CosThetaBetweenArray2(array1, array2):
        sum_square_1 = np.sum((array1**2))**0.5
        sum_square_2 = np.sum((array2**2))**0.5
        dot_product = np.dot(array1, array2)
        cos_theta = dot_product / (sum_square_1 * sum_square_2)
        return cos_theta
    @staticmethod
    # array1 and array2 are not normalized
    @staticmethod
    def ComputeSumSquare(array):
        sum_square = np.sum((array**2))**0.5
        return sum_square
    @staticmethod
    def CosThetaBetweenArray3(dot_product, sum_square_1, sum_square_2):
        cos_theta = dot_product / (sum_square_1 * sum_square_2)
        return cos_theta