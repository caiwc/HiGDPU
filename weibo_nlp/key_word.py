import jieba
import jieba.analyse
from nltk.classify import NaiveBayesClassifier
from os import path
from weibo_nlp.utils import get_content_by_file

d = path.dirname(__file__)
jieba.analyse.set_stop_words(path.join(d, 'stop_word.txt'))
content = get_content_by_file(path.join(d, 'normal.txt'))
a = jieba.analyse.extract_tags(content, 5)
print(a)
b = ['喜欢', '大山', '女生', '点赞', '谢谢', '私聊', '有没有', '校区', '评论', '男生', '广药', '真的', '大学城', '医经', '女朋友', '师妹', '师姐', '同学',
     '中山', '舍友']
c = ['大山', '真的', '喜欢', '请问', '宿舍', '学校', '舍友', '有人', '女生', '感觉', '广药', '不想', '空调', '同学', '图书馆', '校园网', '赤岗', '朋友', '男生',
     '微波炉']
