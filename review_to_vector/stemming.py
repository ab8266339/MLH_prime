from nltk.stem import PorterStemmer

class stemming:

    @staticmethod
    def stemming(word):
        stemmer = PorterStemmer()
        word  = stemmer.stem(word)
        return word