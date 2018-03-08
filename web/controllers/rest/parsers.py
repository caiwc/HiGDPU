from flask_restful import reqparse

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)

official_get_parser = reqparse.RequestParser()
official_get_parser.add_argument('page', type=int, location=['args'])

weibo_get_parser = reqparse.RequestParser()
weibo_get_parser.add_argument('page', type=int, location=['args'])

weixin_get_parser = reqparse.RequestParser()
weixin_get_parser.add_argument('page', type=int, location=['args'])
weixin_get_parser.add_argument('gzh', type=str, location=['args'])

authorization_post_parser = reqparse.RequestParser()
authorization_post_parser.add_argument('code', type=str, required=True)

weibo_post_parser = reqparse.RequestParser()
weibo_post_parser.add_argument(
    'third_session',
    type=str,
    required=True,
    help="third_session is required to edit posts",
)
weibo_post_parser.add_argument(
    'file',
    type=str,
    required=False,
    help="file name"
)
weibo_post_parser.add_argument(
    'content',
    type=str,
    required=True,
    help="content text is required"
)

weibo_put_parser = reqparse.RequestParser()
weibo_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to create posts"
)
weibo_put_parser.add_argument(
    'title',
    type=str
)
weibo_put_parser.add_argument(
    'text',
    type=str
)
weibo_put_parser.add_argument(
    'tags',
    type=str
)

weibo_delete_parser = reqparse.RequestParser()
weibo_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to delete posts"
)
