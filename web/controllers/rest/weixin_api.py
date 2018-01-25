import datetime

from flask import abort
from flask_restful import Resource, fields, marshal_with

from web.models import db, Weixin_Gzh
from .parsers import (
    weibo_get_parser
    #     post_post_parser,
    #     post_put_parser,
    #     post_delete_parser
)

nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}

post_fields = {
    'title_md5': fields.String(),
    'title': fields.String(),
    'html_content': fields.String(),
    'publish_time': fields.DateTime(dt_format='iso8601'),
    'digest': fields.String(),
    'gzh': fields.String(),
    'cover': fields.String(),
    'url': fields.String()
}


class Weixin_Gzh_Api(Resource):
    @marshal_with(post_fields)
    def get(self, gzh_id=None):
        if gzh_id:
            post = Weixin_Gzh.query.filter_by(title_md5=gzh_id).first()
            if not post:
                abort(404)

            return post
        else:
            args = weibo_get_parser.parse_args()
            page = args['page'] or 1

            posts = Weixin_Gzh.query.order_by(
                Weixin_Gzh.publish_time.desc()
            ).paginate(page, 10)

            return posts.items
