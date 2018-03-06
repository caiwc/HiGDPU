from flask import abort, jsonify
from flask_restful import Resource, fields, marshal_with
from web.tasks import send_weibo
from web.models import db, Weibo, User
from web import config
from .parsers import (
    weibo_get_parser,
    weibo_post_parser,
    weibo_put_parser,
    weibo_delete_parser
)

import os

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
    def get(self, weibo_id=None):
        if weibo_id:
            post = Weibo.query.filter_by(weibo_id=weibo_id).first()
            if not post:
                abort(404)

            return jsonify(Weibo.to_dict(post, detail=True))
        else:
            args = weibo_get_parser.parse_args()
            page = args['page'] or 1
            posts = Weibo.query.order_by(
                Weibo.publish_time.desc()
            ).paginate(page, 30).items
            return jsonify(Weibo.to_list(ms=posts, detail=False))

    def post(self):
        args = weibo_post_parser.parse_args(strict=True)
        third_session = args['third_session']
        flag, data = User.verify_auth_3rdsession(thirdsession=third_session)
        if not flag:
            return data['msg']
        content = args['content']
        file = args.get('file', None)
        if file:
            file = os.path.join(config.UPLOAD_PATH, file)
        send_weibo.apply_async(kwargs={'user': data, 'content': content, 'file': file})
