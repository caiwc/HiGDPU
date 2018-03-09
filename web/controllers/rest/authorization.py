from flask import abort, jsonify, session
from flask_restful import Resource
from web.models import User
from web.controllers import api_tool
from .parsers import (
    authorization_post_parser,
)


class Authorization_Api(Resource):
    def post(self):
        args = authorization_post_parser.parse_args()
        js_code = args['code']
        flag, res, meta = api_tool.weixin_authorization(js_code=js_code)
        if flag:
            user = User.add(third_session=meta['third_session'], expires_in=meta['expires_in'],
                               session_key=meta['session_key'], openid=meta['openid'])
            session['user_id'] = user.openid
            session['is_authorization'] = False
            session['third_session'] = user.third_session
            return jsonify(res)
        else:
            return abort(400, {'error': res})
