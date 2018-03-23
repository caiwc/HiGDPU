import jieba
import jieba.analyse
from os import path

d = path.dirname(__file__)
stop_words_path = path.join(d, 'stop_word.txt')
jieba.analyse.set_stop_words(stop_words_path)


def get_stop_word_set():
    res = set()
    f = open(stop_words_path, 'r')
    while True:
        word = f.readline()
        word = word.strip()
        if not word:
            break
        res.add(word)
    f.close()
    return res


def get_content_by_file(file_path):
    f = open(file_path,'r')
    content = []
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n').strip('\u200b').strip('\n')
        if line:
            content.append(line)
    return " ".join(content)

if __name__ == '__main__':
    print(len(get_stop_word_set()))