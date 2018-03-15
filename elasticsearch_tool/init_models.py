# -*- coding: utf-8 -*-

from elasticsearch_dsl import DocType, Text, Keyword, Date, Integer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# Define a default Elasticsearch client
connections.create_connection(hosts=['193.112.112.228'])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowercase'])


class Weibo(DocType):
    suggest = Completion(analyzer=ik_analyzer, search_analyzer=ik_analyzer)
    content = Text(analyzer='ik_max_word', search_analyzer="ik_max_word")
    publish_time = Date()
    comments = Integer()

    class Meta:
        index = 'weibo'
        doc_type = 'shudong'

    @classmethod
    def add_comment(cls, weibo_id, add=True):
        weibo = cls.get(id=weibo_id)
        if add:
            num = 1
        else:
            num = -1
        weibo.comment = weibo.comment + num
        weibo.save()


class Weixin(DocType):
    title = Text(analyzer="ik_max_word")
    content = Text(analyzer='ik_max_word', search_analyzer="ik_max_word")
    url = Keyword()
    cover = Keyword()
    gzh = Keyword()
    digest = Text(analyzer="ik_max_word")
    publish_time = Date()

    class Meta:
        index = 'weixin'
        doc_type = 'gzh'


def get_suggests(index, info_tuple, model):
    es = connections.get_connection(model._doc_type.using)
    used_word = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            word = es.indices.analyze(index=index, body={
                "analyzer": "ik_max_word",
                "text": text,
                "filter": ["lowercase", "asciifolding"],
            })
            analyzed_word = set(r['token'] for r in word["tokens"] if len(r['token']) > 1)
            new_word = analyzed_word - used_word
        else:
            new_word = set()

        if new_word:
            suggests.append({"input": list(new_word), "weight": weight})

    return suggests


if __name__ == '__main__':
    Weibo.init()
