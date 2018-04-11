from flask import abort, jsonify, session
from flask_restful import Resource
from web.models import db, Message,User
from web import config
from .parsers import (
    message_get_parser,
)


class Message_Api(Resource):
    def get(self):
        args = message_get_parser.parse_args()
        page = args['page'] or 1
        not_read = args['not_read'] or True
        if int(not_read) == 0:
            not_read = False
        else:
            not_read = True
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"error": session.get('error')})
        openid = session.get('user_id', None)
        user = User.get(openid=openid)
        color_level = user.get_color_level()
        color_dict = config.color_level_dict[color_level]
        msg_list, all_pages, total = Message.list(user_id=session['user_id'], page=page, not_read=not_read)
        res = {
            "pages": all_pages,
            "total": total,
            "now_page": page,
            "msg": msg_list,
        }
        res.update(color_dict)
        return jsonify(res)
