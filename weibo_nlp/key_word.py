import jieba
import jieba.analyse
from weibo_nlp.utils import get_word_freq
from os import path
from weibo_nlp.utils import get_content_by_file

d = path.dirname(__file__)


def main():
    jieba.analyse.set_stop_words(path.join(d, 'stop_word.txt'))

    content = get_content_by_file(path.join(d, 'sen_txt', 'neg.txt'))
    a = jieba.analyse.extract_tags(content, 20)
    b = jieba.analyse.textrank(content, 20)
    print(a)
    print(b)


def word_freq_to_txt():
    word_freq = get_word_freq()
    output = open(path.join(d, 'word_freq.txt'), 'w', encoding='utf-8')
    for word, freq in word_freq.items():
        output.write("{0} {1}".format(word, freq) + '\n')
    output.close()


if __name__ == '__main__':
    main()
