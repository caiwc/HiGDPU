import datetime

from flask import abort, jsonify
from flask_restful import Resource, fields, marshal_with

from web.models import db, Weixin_Gzh
from .parsers import (
    weixin_get_parser
    #     post_post_parser,
    #     post_put_parser,
    #     post_delete_parser
)


class Weixin_Gzh_Api(Resource):
    def get(self, article_id=None):
        if article_id:
            post = Weixin_Gzh.query.filter_by(title_md5=article_id).first()
            if not post:
                abort(404)

            return jsonify(Weixin_Gzh.to_dict(post, detail=True))
        else:
            args = weixin_get_parser.parse_args()
            page = args['page'] or 1
            gzh = args.get('gzh', None)
            query = Weixin_Gzh.query
            if gzh:
                query = query.filter_by(gzh=gzh)
            posts = query.order_by(
                Weixin_Gzh.publish_time.desc()
            ).paginate(page, 10)
            resp = jsonify(Weixin_Gzh.to_list(posts))
            return resp
