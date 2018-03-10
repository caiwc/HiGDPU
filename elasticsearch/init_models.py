# -*- coding: utf-8 -*-

from elasticsearch_dsl import DocType, Text
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
    content_suggest = Completion(analyzer=ik_analyzer, search_analyzer=ik_analyzer)
    content = Text(analyzer='ik_max_word', search_analyzer="ik_max_word")

    class Meta:
        index = 'weibo'
        doc_type = 'shudong'

if __name__ == '__main__':
    Weibo.init()