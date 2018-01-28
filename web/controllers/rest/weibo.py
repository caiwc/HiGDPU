import datetime

from flask import abort
from flask_restful import Resource, fields, marshal_with

from web.models import db, Weibo
from .parsers import (
    weibo_get_parser,
    weibo_post_parser,
    weibo_put_parser,
    weibo_delete_parser
)

# from .fields import HTMLField


post_fields = {
    'weibo_id': fields.String(),
    'content': fields.String(),
    'publish_time': fields.DateTime(dt_format='iso8601'),
    'weibo_name': fields.String(),
    'reposts': fields.Integer(),
    'likes': fields.Integer(),
    'comments': fields.Integer()
}


class Weibo_Api(Resource):
    @marshal_with(post_fields)
    def get(self, weibo_id=None):
        if weibo_id:
            post = Weibo.query.filter_by(weibo_id=weibo_id).first()
            if not post:
                abort(404)

            return post
        else:
            args = weibo_get_parser.parse_args()
            page = args['page'] or 1
            posts = Weibo.query.order_by(
                Weibo.publish_time.desc()
            ).paginate(page, 30)
            return posts.items

    def post(self, post_id=None):
        pass