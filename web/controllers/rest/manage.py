from flask import abort, jsonify, session
from flask_restful import Resource
from web.models import db, Message, User
from .parsers import (
    manage_post_parser,
)

delete_weibo_reason = {
    "user_apply": "用户申请删除"
}


class Manager_Api(Resource):
    def get(self):
        args = manage_post_parser.parse_args()
        page = args['page'] or 1
        not_read = args['not_read'] or True
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"error": session.get('error')})
        msg_list = Message.list(user_id=session['user_id'], page=page, not_read=not_read)
        return jsonify(Message.to_list(ms=msg_list, detail=False))

    def post(self):
        args = manage_post_parser.parse_args()
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"error": session.get('error')})
        user = User.get(openid=session.get('user_id'))
        assert isinstance(user, User)
        if not user.manager:
            return abort(400, {"error": "此操作只有管理员能执行"})

        weibo_id = args['weibo_id']
        reason = args['reason']
