import jieba
import jieba.analyse
from weibo_nlp.utils import get_word_freq, get_content_by_file, get_stop_word_set
from os import path
import math
from web.models import Weibo

d = path.dirname(__file__)
stop_set = get_stop_word_set()
all_word_path = path.join(d, 'word', 'word_2c_done.txt')


def get_key_word(weibo_query=None):
    cut_word_path = path.join(d, 'cut_word.txt')
    jieba.load_userdict(cut_word_path)
    jieba.analyse.set_stop_words(path.join(d, 'stop_word.txt'))
    jieba.analyse.set_idf_path(path.join(d, 'word_idf.txt'))
    all_content = ""
    content_list = [o.content for o in weibo_query.all()]
    all_count = len(content_list)
    for content in content_list:
        content_cut = jieba.cut(content, cut_all=False)
        content_str = " ".join(content_cut)
        all_content = all_content + content_str
    # all_content = get_content_by_file(path.join(d, 'sen_txt', 'trade.txt'))
    key_word_list = jieba.analyse.extract_tags(all_content, 30)
    b = jieba.analyse.textrank(all_content, 20)
    res = []
    for word in key_word_list:
        word_count = weibo_query.filter(Weibo.content.contains(word)).count()
        has_word = word_count/all_count
        if has_word >= 0.025:
            res.append(word)
    print(key_word_list[:5])
    print(b)
    return res[:5]


def word_freq_to_txt():
    word_freq = get_word_freq()
    output = open(path.join(d, 'word_freq.txt'), 'w', encoding='utf-8')
    for word, freq in word_freq.items():
        output.write("{0} {1}".format(word, freq) + '\n')
    output.close()


def save(idf_dict):
    f_path = path.join(d, "word_idf.txt")
    f = open(f_path, "a+")
    f.truncate()
    # write_list = []
    for key in idf_dict.keys():
        # write_list.append(str(key)+" "+str(idf_dict[key]))
        f.write(str(key) + " " + str(idf_dict[key]) + "\n")
    f.close()


def docs(w, D):
    c = 0
    for d in D:
        if w in d:
            c = c + 1
    return c


def compute_idf(f_path):
    # 所有分词后文档
    D = []
    # 所有词的set
    W = set()
    f = open(f_path, 'r')
    idx = 1
    while True:
        content = f.readline()
        if not content.strip():
            break
        d = content.split(" ")
        d = set([o.strip() for o in d if o not in stop_set])
        D.append(d)
        W = W | d
        print('read file {}'.format(idx))
        idx += 1
    f.close()
    print('finish')
    # 计算idf
    idf_dict = {}
    n = len(W)
    # idf = log(n / docs(w, D))
    for w in list(W):
        idf = math.log(n * 1.0 / docs(w, D))
        idf_dict[w] = idf
        print('get {} idf:{}'.format(w, idf))
    return idf_dict


def get_idf():
    # 得到idf的字典
    idf_dict = compute_idf(all_word_path)
    save(idf_dict)


if __name__ == '__main__':
    get_key_word()
