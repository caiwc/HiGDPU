from flask import abort, jsonify
from flask_restful import Resource
from web.models import db, Message, User
from .parsers import (
    message_get_parser,
)


class Message_Api(Resource):
    def get(self, article_id=None):
        if article_id:
            post = Message.query.filter_by(article_id=article_id).first()
            if not post:
                abort(404)

            return jsonify(Message.to_dict(post, detail=True))
        else:
            args = message_get_parser.parse_args()
            page = args['page'] or 1
            posts = Message.query.order_by(
                Message.publish_time.desc()
            ).paginate(page, 30).items
            return jsonify(Message.to_list(ms=posts, detail=False))
