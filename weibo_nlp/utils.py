import jieba
import jieba.analyse
from os import path

d = path.dirname(__file__)
stop_words_path = path.join(d, 'stop_word.txt')
stop_symbol_path = path.join(d, 'stop_symbol.txt')
cut_word_path = path.join(d, 'cut_word.txt')
jieba.analyse.set_stop_words(stop_words_path)


def get_stop_word_set(symbol=False):
    res = set()
    if not symbol:
        f = open(stop_words_path, 'r')
    else:
        f = open(stop_symbol_path, 'r')
    while True:
        word = f.readline()
        word = word.strip()
        if not word:
            break
        res.add(word)
    f.close()
    return res


def get_content_by_file(file_path):
    f = open(file_path, 'r')
    content = []
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip('\n').strip('\u200b').strip('\n')
        if line:
            content.append(line)
    return " ".join(content)


def is_alpha(tok):
    try:
        return tok.encode('ascii').isalpha()
    except UnicodeEncodeError:
        return False


def get_word_freq():
    from nltk.probability import FreqDist
    word_fd = FreqDist()
    i = 0
    print('Start...')
    with open(path.join(d, 'word', 'word2c.txt'), 'r', encoding='utf-8') as raw_input:
        for line in raw_input.readlines():
            line = line.strip()
            i += 1
            print('line ' + str(i))
            text = line.split()
            if True:
                text = [w for w in text if not is_alpha(w)]
            word_cut_seed = [jieba.cut(t, cut_all=True) for t in text]
            for sent in word_cut_seed:
                for tok in sent:
                    word_fd[tok] += 1
    return word_fd


def sort_idf():
    idf_path = path.join(d, 'word_idf.txt')
    word_dict = list()
    with open(idf_path, 'r') as f:
        for line in f.readlines():
            word_line = line.split(' ')
            word = word_line[0]
            idf = word_line[1]
            word_dict.append({'word': word, 'idf': idf})

    word_dict = sorted(word_dict, key=lambda x: x['idf'])

    new_idf_path = path.join(d, 'sort_word_idf.txt')
    new_f = open(new_idf_path, 'w')
    for word_idf in word_dict:
        new_f.write(word_idf['word'] + ' ' + word_idf['idf'])
    new_f.close()

if __name__ == '__main__':
    sort_idf()
