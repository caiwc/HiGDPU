import pickle
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from random import shuffle
import itertools
from collections import namedtuple
import jieba
from nltk.classify import NaiveBayesClassifier


def bigrams_words_feature(words, nbigrams=200, measure=BigramAssocMeasures.chi_sq):
    bigrams_finder = BigramCollocationFinder.from_documents(words)
    bigrams = bigrams_finder.nbest(measure, nbigrams)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])


Review = namedtuple("Review", 'text tags')


def get_reviews(file_path, tag):
    res = []
    f = open(file_path, 'r')
    idx = 0
    content = []
    while True:
        line = f.readline()
        if not line:
            break
        if line == '\n':
            res.append(Review([i for i in jieba.cut("".join(content), cut_all=False)], "{}_{}".format(tag, idx)))
            idx += 1
            content = []
            continue
        content.append(line)
    f.close()
    return res


def main():
    neg_file_path = "/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/neg.txt"
    pos_file_path = "/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/pos.txt"
    else_file_path = "/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/else.txt"
    reviews_neg = get_reviews(neg_file_path, 'neg')
    reviews_pos = get_reviews(pos_file_path, 'pos')

    print(len(reviews_neg), len(reviews_pos))

    negfeature = [(bigrams_words_feature(r.text, 5), 'neg') for r in reviews_neg]
    posfeature = [(bigrams_words_feature(r.text, 5), 'pos') for r in reviews_pos]

    shuffle(posfeature)
    shuffle(negfeature)
    portionpos = int(len(posfeature) * 0.8)
    portionneg = int(len(negfeature) * 0.8)


    print(portionpos, '-', portionneg)

    trainfeatures = negfeature[:portionpos] + posfeature[:portionneg]

    print(len(trainfeatures))
    shuffle(trainfeatures)
    classifier = NaiveBayesClassifier.train(trainfeatures)

    testfeature = negfeature[portionneg:] + posfeature[portionpos:]

    shuffle(testfeature)

    err = 0
    print("test", len(testfeature))

    for r in testfeature:
        sent = classifier.classify(r[0])
        if sent != r[1]:
            err += 1

    print("error rate:", err / float(len(testfeature)))

    f = open('/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/my_nlp.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()


if __name__ == '__main__':
    main()
