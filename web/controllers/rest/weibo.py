from flask import abort, jsonify, request
from flask_restful import Resource
from web.tasks import send_weibo, send_weibo_comment
from web.models import db, Weibo, User
from web import config
from .parsers import (
    weibo_get_parser,
    weibo_post_parser,
    weibo_put_parser,
    weibo_delete_parser
)

import os


class Weibo_Api(Resource):
    def get(self, weibo_id=None):
        if weibo_id:
            post = Weibo.query.filter_by(weibo_id=weibo_id).first()
            if not post:
                abort(404, {'error': '不存在此id的微博'})

            return jsonify(Weibo.to_dict(post, detail=True))
        else:
            args = weibo_get_parser.parse_args()
            page = args['page'] or 1
            posts = Weibo.query.order_by(
                Weibo.publish_time.desc()
            ).paginate(page, 30).items
            return jsonify(Weibo.to_list(ms=posts, detail=False))

    def post(self):
        request_path = request.full_path
        path_list = request_path.split('/')
        args = weibo_post_parser.parse_args(strict=True)
        third_session = args['third_session']
        flag, data = User.verify_auth_3rdsession(thirdsession=third_session)
        if not flag:
            return abort(401, data)
        if path_list[-1] == 'comment':
            content = args['content']
            weibo_id = args['weibo_id']
            reply_author = args.get('reply_author', None)
            reply_comment_id = args.get('reply_comment_id', None)
            send_weibo_comment.apply_async(
                kwargs={'user': data, 'content': content, 'weibo_id': weibo_id, 'reply_author': reply_author,
                        'reply_comment_id': reply_comment_id})
            return jsonify({'msg': 'success'})
        else:
            content = args['content']
            file = args.get('file', None)
            if file:
                file = os.path.join(config.UPLOAD_PATH, file)
            send_weibo.apply_async(kwargs={'user': data, 'content': content, 'file': file})
            return jsonify({'msg': 'success'})
