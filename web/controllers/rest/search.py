# coding:utf-8
from flask import abort, jsonify, request
from flask_restful import Resource
from web.models import time_format
from .parsers import search_post_parser
from elasticsearch import Elasticsearch
from web.config import ES_HOST
from elasticsearch_tool.init_models import Weibo

client = Elasticsearch(hosts=[ES_HOST])

search_dict = {
    "weixin": {"field": ["title", "content"], "size": 5},
    "weibo": {"field": ["content"], "size": 5}
}

sort_dict = {
    "time": {
        "publish_time": {
            "order": "desc"
        }
    },
    "score": "_score",
    "comment": {"comment": "desc"}
}


class Search_Api(Resource):
    def post(self):
        args = search_post_parser.parse_args()
        query = args['query']
        request_path = request.path
        # path_list = request_path.split('/')
        # if 'suggest' in path_list[-1]:
        #     re_datas = []
        #     if query:
        #
        #         s = Weibo.search()
        #         res = s.suggest('my_suggest', query, completion={
        #             "field": "suggest", "fuzzy": {
        #                 "fuzziness": 2,
        #                 "prefix_length": 1
        #             },
        #             "size": 5
        #         })
        #         suggestion = res.execute()
        #         for match in suggestion.suggest.my_suggest[0].options:
        #             source = match._source['content']
        #             re_datas.append(source)
        #         return jsonify(re_datas)
        # else:
        page = args['page'] or 1
        search_type = args['type'] or None
        order = args['order'] or 'score'

        if search_type:
            do_search = {search_type: {"field": search_dict[search_type]['field'], "size": 10}}
        else:
            do_search = search_dict
        res = []
        for s_type in sorted(do_search):
            if order == "score":
                sort_list = [sort_dict[order]]
            elif s_type == "weixin" and order == "comment":
                sort_list = [sort_dict["score"]]
            else:
                sort_list = [sort_dict[order], sort_dict['score']]
            # 获取返回数据的排序字段, 将排序字段放入sort_list里

            size = do_search[s_type]['size']
            # 获取返回item的数量
            response = client.search(
                index=s_type,
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": do_search[s_type]['field']
                        }
                    },
                    "from": (page - 1) * size,
                    "size": size,
                    "highlight": {
                        "pre_tags": [''],
                        "post_tags": [""],
                        "fields": {
                            "title": {},
                            "content": {},
                        }
                    },
                    "sort": sort_list
                })
            # 构造请求body,其中指定了以multi_match为搜索方式,field指定搜索查找的字段.from,size表示页数和每页数量大小
            # highlight会自动截取搜索命中的部分,sort指定排序的关键词

            total_nums = response["hits"]["total"]
            if (page % size) > 0:
                page_nums = int(total_nums / size) + 1
            else:
                page_nums = int(total_nums / size)
            # 获取命中item的总数和得出总页数
            hit_list = []
            for hit in response["hits"]["hits"]:
                hit_dict = dict()
                hit_dict["publish_time"] = time_format(hit["_source"]["publish_time"])
                hit_dict["id"] = hit["_id"]
                hit_dict["score"] = hit["_score"]
                hit_dict['type'] = hit["_index"]
                if "content" in hit["highlight"]:
                    hit_dict["content"] = "".join(hit["highlight"]["content"])[:200]
                else:
                    hit_dict["content"] = hit["_source"]["content"][:200]

                if s_type == 'weixin':
                    if "title" in hit["highlight"]:
                        hit_dict["title"] = "".join(hit["highlight"]["title"])
                    else:
                        hit_dict["title"] = hit["_source"]["title"]
                    hit_dict['cover'] = hit["_source"]['cover']
                    hit_dict['gzh'] = hit["_source"]['gzh']
                    hit_dict['url'] = hit["_source"]['url']

                elif s_type == 'weibo':
                    hit_dict["comment"] = hit["_source"].get("comment", 0)
                hit_list.append(hit_dict)
            if not len(hit_list):
                hit_list.append({'content': '没有搜到任何东西'})
            res.append({'pages': page_nums, "total": total_nums, "data": hit_list, "type": s_type})

        return jsonify(res)
