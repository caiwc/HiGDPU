from flask import abort, jsonify, session, request
from flask_restful import Resource
from web.models import db, Message, User, Weibo_to_delete, Weibo
from .parsers import (
    manage_post_parser,
)
from web import config


class Manager_Api(Resource):
    def get(self):
        pass

    def post(self):
        args = manage_post_parser.parse_args()
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"error": session.get('error')})
        user = User.get(openid=session.get('user_id'))
        if not user.manager:
            return abort(400, {"error": "此操作只有管理员能执行"})

        weibo_id = args['weibo_id']
        reason = args['reason']

        weibo = Weibo.get(weibo_id)
        if weibo:
            if weibo.weibo_name != config.WEIBO_NAME:
                return abort(400, {'error': '此微博不由本站管理,不能删除'})
            weibo.status = True
            db.session.add(weibo)

            if reason not in Weibo_to_delete.reason_choices_dict:
                reason = Weibo_to_delete.Others
            weibo_delete = Weibo_to_delete()
            weibo_delete.weibo_id = weibo_id
            weibo_delete.reason = reason
            weibo_delete.done = False
            db.session.add(weibo_delete)

            db.session.commit()

            Message.add(weibo=None, user_id=user.openid,
                        content=config.WEIBO_DELETE_MSG.format(content=weibo.content,
                                                               reason=Weibo_to_delete.reason_choices_dict[reason]))
        return jsonify({'msg': '删除申请成功,微博将在今天内删除'})
