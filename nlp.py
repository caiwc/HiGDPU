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

best_word = "best_word"
best_bigrams = "best_bigrams"


def bigrams_words_feature(words, nbigrams=200, measure=BigramAssocMeasures.chi_sq):
    bigrams_finder = BigramCollocationFinder.from_documents(words)
    bigrams = bigrams_finder.nbest(measure, nbigrams)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])


bestwords = None


def best_word_feature(words):
    global bestwords
    if not bestwords:
        bestwords = best_word_method()
    return dict([word, True] for word in words if word in bestwords)


Review = namedtuple("Review", 'words tags')


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


def process_reviews():
    neg_file_path = "/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/neg_1.txt"
    pos_file_path = "/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/pos_1.txt"
    else_file_path = "/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/else.txt"
    reviews_neg = get_reviews(neg_file_path, 'neg')
    reviews_pos = get_reviews(pos_file_path, 'pos')
    print(len(reviews_neg), len(reviews_pos))
    return reviews_pos, reviews_neg


def best_word_method():
    from nltk.probability import FreqDist, ConditionalFreqDist
    reviews_pos, reviews_neg = process_reviews()

    tot_poswords = [val for l in [r.words for r in reviews_pos] for val in l]
    tot_negwords = [val for l in [r.words for r in reviews_neg] for val in l]

    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()

    for word in tot_poswords:
        word_fd[word] += 1
        label_word_fd['pos'][word] += 1

    for word in tot_negwords:
        word_fd[word] += 1
        label_word_fd['neg'][word] += 1

    pos_words = len(tot_poswords)
    neg_words = len(tot_negwords)

    tot_words = pos_words + neg_words

    word_scores = {}

    for word, freq in word_fd.items():
        pos_scores = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word], (freq, pos_words), tot_words)
        neg_scores = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word], (freq, neg_words), tot_words)
        word_scores[word] = pos_scores + neg_scores
    print('total', len(word_scores))

    best = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:5000]
    bestwords = set([w for w, s in best])
    return bestwords


def get_feature(method):
    reviews_pos, reviews_neg = process_reviews()
    if method == best_bigrams:
        negfeature = [(bigrams_words_feature(r.words, 8), 'neg') for r in reviews_neg]
        posfeature = [(bigrams_words_feature(r.words, 8), 'pos') for r in reviews_pos]
    else:
        posfeature = [(best_word_feature(r.words), 'neg') for r in reviews_neg]
        negfeature = [(best_word_feature(r.words), 'pos') for r in reviews_pos]
    return posfeature, negfeature


def main():
    posfeature, negfeature = get_feature(method=best_word)
    shuffle(posfeature)
    shuffle(negfeature)
    portionpos = int(len(posfeature) * 0.8)
    portionneg = int(len(negfeature) * 0.8)

    print(portionpos, '-', portionneg)

    trainfeatures = negfeature[:portionpos] + posfeature[:portionneg]

    print('train_count', len(trainfeatures))
    shuffle(trainfeatures)
    classifier = NaiveBayesClassifier.train(trainfeatures)

    testfeature = negfeature[portionneg:] + posfeature[portionpos:]

    shuffle(testfeature)

    err = 0
    print("test", len(testfeature))

    for r in testfeature:
        sent = classifier.classify(r[0])
        a = classifier.prob_classify(r[0])
        if sent != r[1]:
            err += 1

    print("error rate:", err / float(len(testfeature)))

    f = open('/Users/caiweicheng/self/venv/HiGDPU/weibo_nlp/my_nlp1.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()


def doc2v():
    from gensim.models import Doc2Vec
    import multiprocessing
    reviews_pos, reviews_neg = process_reviews()
    tot_reviews = reviews_pos + reviews_neg
    shuffle(tot_reviews)
    cores = multiprocessing.cpu_count()
    vec_size = 500
    model_d2v = Doc2Vec(dm=1, dm_concat=0, vector_size=vec_size, window=5, negative=0, hs=0, min_count=1, workers=cores)

    # build vocab
    model_d2v.build_vocab(tot_reviews)
    # train
    numepochs = 20
    for epoch in range(numepochs):
        try:
            print('epoch %d' % (epoch))
            model_d2v.train(tot_reviews, total_words=len(tot_reviews), epochs=epoch)
            model_d2v.alpha *= 0.99
            model_d2v.min_alpha = model_d2v.alpha
        except (KeyboardInterrupt, SystemExit):
            break

    import numpy as np
    trainingsize = 2 * int(len(reviews_pos) * 0.8)

    train_d2v = np.zeros((trainingsize, vec_size))
    train_labels = np.zeros(trainingsize)
    test_size = len(tot_reviews) - trainingsize
    test_d2v = np.zeros((test_size, vec_size))
    test_labels = np.zeros(test_size)

    cnt_train = 0
    cnt_test = 0
    for r in reviews_pos:
        name_pos = r.tags
        if int(name_pos.split('_')[1]) >= int(trainingsize / 2.):
            test_d2v[cnt_test] = model_d2v.docvecs[name_pos]
            test_labels[cnt_test] = 1
            cnt_test += 1
        else:
            train_d2v[cnt_train] = model_d2v.docvecs[name_pos]
            train_labels[cnt_train] = 1
            cnt_train += 1

    for r in reviews_neg:
        name_neg = r.tags
        if int(name_neg.split('_')[1]) >= int(trainingsize / 2.):
            test_d2v[cnt_test] = model_d2v.docvecs[name_neg]
            test_labels[cnt_test] = 0
            cnt_test += 1
        else:
            train_d2v[cnt_train] = model_d2v.docvecs[name_neg]
            train_labels[cnt_train] = 0
            cnt_train += 1

    from sklearn.linear_model import LogisticRegression
    classifier = LogisticRegression()
    classifier.fit(train_d2v, train_labels)
    print('accuracy:', classifier.score(test_d2v, test_labels))

    from sklearn.svm import SVC
    clf = SVC()
    clf.fit(train_d2v, train_labels)
    print('accuracy:', clf.score(test_d2v, test_labels))


if __name__ == '__main__':
    doc2v()
