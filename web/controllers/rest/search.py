from flask import abort, jsonify
from flask_restful import Resource
from web.models import db, Weibo, User
from .parsers import search_get_parser


class Search_Api(Resource):
    def get(self):
        args = search_get_parser.parse_args()
        page = args['page'] or 1
        search_type = args['type'] or None
        order = args['order'] or 'time'
