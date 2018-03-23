from flask import abort, jsonify, request, session
from flask_restful import Resource
from web.tasks import send_weibo, send_weibo_comment
from web.models import db, Weibo, User, Message, Weibo_to_delete, Tag
from web import config
from .parsers import (
    weibo_get_parser,
    weibo_post_parser,
    weibo_comment_post_parser,
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
            tag = args['tag'] or None
            if tag:
                posts = Weibo.query.filter(Weibo.tags.any(Tag.name == tag))
            else:
                posts = Weibo.query
            posts = posts.order_by(
                Weibo.publish_time.desc()
            ).paginate(page, 30)
            msg_count = Message.new_msg_count(user_id=session.get('user_id', ''))
            weibo_list = Weibo.to_list(ms=posts.items, detail=False)
            res = {
                "pages": posts.pages,
                "total": posts.total,
                "msg_count": msg_count,
                "weibo": weibo_list
            }
            return jsonify(res)

    def post(self):
        request_path = request.path
        path_list = request_path.split('/')
        if 'comment' in path_list[-1]:
            args = weibo_comment_post_parser.parse_args(strict=True)
        else:
            args = weibo_post_parser.parse_args(strict=True)
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"error": session.get('error')})
        user = User.get(openid=session.get('user_id'))
        if path_list[-1] == 'comment':
            content = args['content']
            weibo_id = args['weibo_id']
            reply_author = args.get('reply_author_name', None)
            reply_author_id = args.get('reply_author_id', None)
            reply_comment_id = args.get('reply_comment_id', None)
            # send_weibo_comment.apply_async(
            #     kwargs={'user': user, 'content': content, 'weibo_id': weibo_id, 'reply_author': reply_author,
            #             'reply_author_id': reply_author_id, 'reply_comment_id': reply_comment_id})
            send_weibo_comment(user=user,content=content,weibo_id=weibo_id,reply_author=reply_author,reply_comment_id=reply_comment_id,reply_author_id=reply_author_id)
            return jsonify({'msg': 'success'})

        else:
            if user.is_over_post():
                return abort(400, {"error": "你发送微博过于频繁,请稍后再发"})

            content = args['content']
            file = args.get('file', None)
            if file:
                file = os.path.join(config.UPLOAD_PATH, file)
            # send_weibo.apply_async(kwargs={'user': user, 'content': content, 'file': file})
            send_weibo(user=user,content=content,file=file)
            return jsonify({'msg': 'success'})

    def delete(self):
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"error": session.get('error')})
        user_id = session.get('user_id')
        args = weibo_delete_parser.parse_args(strict=True)
        weibo_id = args['weibo_id']
        weibo = Weibo.query.filter_by(weibo_id=weibo_id).first()
        if not weibo:
            return abort(400, {'error': '无此微博'})
        if weibo.author != user_id:
            return abort(403, {'error': '此微博作者不是本人, 不能删除'})
        weibo.status = True
        db.session.add(weibo)

        weibo_delete = Weibo_to_delete()
        weibo_delete.reason = Weibo_to_delete.Self_apply
        weibo_delete.weibo_id = weibo_id
        weibo_delete.done = False
        db.session.add(weibo_delete)
        db.session.commit()

        Message.add(weibo=None, user_id=User.get_manager_user_id(),
                    content=config.WEIBO_APPLY_DELETE_MSG.format(content=weibo.content))
        return jsonify({'msg': '删除申请成功,微博将在今天内删除'})
