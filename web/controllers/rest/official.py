from flask import abort, jsonify
from flask_restful import Resource
from web.models import db, Official, User
from .parsers import (
    official_get_parser,
)


class Official_Api(Resource):
    def get(self, article_id=None):
        if article_id:
            post = Official.query.filter_by(article_id=article_id).first()
            if not post:
                abort(404)

            return jsonify(Official.to_dict(post, detail=True))
        else:
            args = official_get_parser.parse_args()
            page = args['page'] or 1
            posts = Official.query.order_by(
                Official.publish_time.desc()
            ).paginate(page, 30).items
            return jsonify(Official.to_list(ms=posts, detail=False))
