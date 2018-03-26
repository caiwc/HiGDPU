from flask import abort, jsonify
from flask_restful import Resource
from elasticsearch_tool.init_models import Weixin
from elasticsearch.exceptions import NotFoundError
from .parsers import weixin_get_parser
from web.extensions import cache
from web.models import time_format


class Weixin_Gzh_Api(Resource):
    @cache.cached(timeout=60)
    def get(self, article_id=None):
        if article_id:
            try:
                item = Weixin.get(id=article_id)
                tmp = {}
                tmp['id'] = item._id
                tmp['title'] = item.title
                tmp['url'] = item.url
                tmp['publish_time'] = time_format(item.publish_time)
                tmp['digest'] = item.digest
                tmp['cover'] = item.cover
                tmp['gzh'] = item.gzh
                return jsonify(tmp)
            except NotFoundError:
                return abort(404)
        else:
            args = weixin_get_parser.parse_args()
            page = args['page'] or 1
            gzh = args.get('gzh', None)
            start = (page - 1) * 10
            end = page * 10
            res = []
            s = Weixin.search().query()
            if gzh:
                s = s.query("match", gzh=gzh)
            s = s.sort('-publish_time')
            s.execute()
            for hit in s[start:end]:
                tmp = {}
                tmp['id'] = hit._id
                tmp['title'] = hit.title
                tmp['url'] = hit.url
                tmp['publish_time'] = time_format(hit.publish_time)
                tmp['digest'] = hit.digest
                tmp['cover'] = hit.cover
                tmp['gzh'] = hit.gzh
                res.append(tmp)
            total_nums = s.count()
            if (page % 10) > 0:
                page_nums = int(total_nums / 10) + 1
            else:
                page_nums = int(total_nums / 10)

            return jsonify({
                'total': total_nums,
                'pages': page_nums,
                'data': res
            })
