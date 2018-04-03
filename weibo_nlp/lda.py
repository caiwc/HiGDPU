import gensim.models
from gensim import models, corpora
from nltk.stem.porter import PorterStemmer
import pickle
from os import path
import jieba
import copy
from weibo_nlp.utils import cut_word_path, get_stop_word_set

d = path.dirname(__file__)
jieba.load_userdict(cut_word_path)
stemmer = PorterStemmer()
stop_list = get_stop_word_set()

times = 1


class GenSimCorpus(object):
    def __init__(self, texts, stoplist=[], bestwords=[]):
        self.texts = texts
        self.stoplist = stoplist
        self.bestwords = bestwords
        self.dictionary = gensim.corpora.Dictionary(self.iter_docs(texts, stoplist))

    def __len__(self):
        return len(self.texts)

    def __iter__(self):
        for tokens in self.iter_docs(self.texts, self.stoplist):
            yield self.dictionary.doc2bow(tokens)
        global times
        times += 1

    def iter_docs(self, texts, stoplist):
        for idx, text in enumerate(texts):
            print('No.{} cut {}'.format(times, idx + 1))
            if len(self.bestwords) > 0:
                yield (x for x in jieba.cut(text, cut_all=False) if x in self.bestwords)
            else:
                yield (x for x in jieba.cut(text, cut_all=False) if x not in stoplist)


def get_weibo_list(cut=False):
    all_weibo_path = path.join(d, 'word', 'word2c.txt')
    all_weibo_list = []
    i = 1
    with open(all_weibo_path, 'r', encoding='utf-8') as raw_input:
        for line in raw_input.readlines():
            line = line.strip()
            i += 1
            print('line ' + str(i))
            if line:
                if not cut:
                    all_weibo_list.append(line)
                else:
                    text = []
                    for x in jieba.cut(line, cut_all=False):
                        x = x.strip().strip('\u200b').strip()
                        if x:
                            text.append(x)
                    all_weibo_list.append(text)

    return all_weibo_list


def lda():
    num_topics = 8
    all_weibo = get_weibo_list()
    corpus = GenSimCorpus(all_weibo, stop_list, [])
    dict_lda = corpus.dictionary
    lda = models.LdaModel(corpus, num_topics=num_topics, id2word=dict_lda, passes=1, iterations=50)

    lda.show_topics(num_topics=num_topics)

    # filter out very common words like mobie and film or very unfrequent terms
    out_ids = [tokenid for tokenid, docfreq in dict_lda.dfs.items() if docfreq > 1000 or docfreq < 3]
    dict_lfq = copy.deepcopy(dict_lda)
    dict_lfq.filter_tokens(out_ids)
    dict_lfq.compactify()
    corpus = [dict_lfq.doc2bow(jieba.cut(text, cut_all=False)) for text in all_weibo]

    lda_lfq = models.LdaModel(corpus, num_topics=num_topics, id2word=dict_lfq, passes=10, iterations=50, alpha=0.01,
                              eta=0.01)
    for t in range(num_topics):
        print('topic ', t, '  words: ', lda_lfq.print_topic(t, topn=8))

    f = open(path.join(d, 'lda.pickle'), 'wb')
    pickle.dump(lda_lfq, f)
    f.close()


def lda2():
    num_topics = 10
    texts = get_weibo_list(True)
    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]

    # out_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq > 1000 or docfreq < 3]
    # dict_lfq = copy.deepcopy(dictionary)
    # dict_lfq.filter_tokens(out_ids)
    # dict_lfq.compactify()

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary.dfs, passes=50)

    for t in range(num_topics):
        print('topic ', t, '  words: ', ldamodel.print_topic(t, topn=num_topics))

    f = open(path.join(d, 'lda.pickle'), 'wb')
    pickle.dump(ldamodel, f)
    f.close()


if __name__ == '__main__':
    lda2()
