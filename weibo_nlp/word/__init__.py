from gensim.models import Word2Vec
from os import path

d = path.dirname(__file__)

word2vec = Word2Vec.load(path.join(d, 't2s.model'))

