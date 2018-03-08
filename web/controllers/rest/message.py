from flask import abort, jsonify, session
from flask_restful import Resource
from web.models import db, Message
from .parsers import (
    message_get_parser,
)


class Message_Api(Resource):
    def get(self):
        args = message_get_parser.parse_args()
        page = args['page'] or 1
        not_read = args['not_read'] or True
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"error": session.get('error')})
        msg_list = Message.list(user_id=session['user_id'], page=page, not_read=not_read)
        return jsonify(Message.to_list(ms=msg_list, detail=False))
