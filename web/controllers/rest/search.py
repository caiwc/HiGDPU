# coding:utf-8
from flask import abort, jsonify, request
from flask_restful import Resource
from web.models import db, Weibo, User
from .parsers import search_get_parser
from elasticsearch import Elasticsearch
from web.config import ES_HOST
from elasticsearch_tool.init_models import Weibo

client = Elasticsearch(hosts=[ES_HOST])


class Search_Api(Resource):
    def get(self):
        args = search_get_parser.parse_args()
        query = args['query']
        request_path = request.path
        path_list = request_path.split('/')
        if 'suggest' in path_list[-1]:
            re_datas = []
            if query:

                s = Weibo.search()
                res = s.suggest('my_suggest', query, completion={
                    "field": "suggest", "fuzzy": {
                        "fuzziness": 2,
                        "prefix_length": 1
                    },
                    "size": 5
                })
                suggestion = res.execute()
                for match in suggestion.suggest.my_suggest[0].options:
                    source = match._source['content']
                    re_datas.append(source)
                return jsonify(re_datas)
        else:
            page = args['page'] or 1
            search_type = args['type'] or None
            order = args['order'] or 'time'

            response = client.search(
                index=search_type,
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "content"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                    "highlight": {
                        "pre_tags": ['<span class="keyWord">'],
                        "post_tags": ['</span>'],
                        "fields": {
                            "title": {},
                            "content": {},

                        }
                    }
                }
            )
            hit_list = []
            total_nums = response["hits"]["total"]
            if (page % 10) > 0:
                page_nums = int(total_nums / 10) + 1
            else:
                page_nums = int(total_nums / 10)
            for hit in response["hits"]["hits"]:
                hit_dict = {}

                if "title" in hit["highlight"]:
                    hit_dict["title"] = "".join(hit["highlight"]["title"])
                elif "title" in hit["_source"]:
                    hit_dict["title"] = hit["_source"]["title"]
                if "content" in hit["highlight"]:
                    hit_dict["content"] = "".join(hit["highlight"]["content"])[:200]
                else:
                    hit_dict["content"] = hit["_source"]["content"][:200]

                hit_dict["publish_time"] = hit["_source"]["publish_time"]
                hit_dict["id"] = hit["_id"]
                hit_dict["score"] = hit["_score"]
                hit_dict['type'] = hit["_index"]
                hit_list.append(hit_dict)
            res = {"total": total_nums, "page_nums": page_nums, "data": hit_list}
            return jsonify(res)
