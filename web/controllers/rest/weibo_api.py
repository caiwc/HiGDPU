import datetime

from flask import abort
from flask_restful import Resource, fields, marshal_with

from web.models import db, Weibo
# from .parsers import (
#     post_get_parser,
#     post_post_parser,
#     post_put_parser,
#     post_delete_parser
# )
# from .fields import HTMLField

nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}

post_fields = {
    'id': fields.Integer(),
    'content': fields.String(),

    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_time': fields.DateTime(dt_format='iso8601')
}


class Weibo_Api(Resource):
    @marshal_with(post_fields)
    def get(self, post_id=None):
        if post_id:
            post = Weibo.query.get(post_id)
            if not post:
                abort(404)

            return post
        else:
            posts = Weibo.query.order_by(
                Weibo.publish_time.desc()
            )
            return posts
        pass

    def post(self, post_id=None):
        pass

    def put(self, post_id=None):
        pass

    def delete(self, post_id=None):
       pass
