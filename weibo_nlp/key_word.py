import jieba
import jieba.analyse
from nltk.classify import NaiveBayesClassifier
from os import path

d = path.dirname(__file__)
jieba.analyse.set_stop_words(path.join(d, 'stop_word.txt'))