from flask_restful import reqparse

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)

weibo_get_parser = reqparse.RequestParser()
weibo_get_parser.add_argument('page', type=int, location=['args', 'headers'])
weibo_get_parser.add_argument('user', type=str, location=['args', 'headers'])

weibo_post_parser = reqparse.RequestParser()
weibo_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help="Auth Token is required to edit posts"
)
weibo_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    help="Title is required"
)
weibo_post_parser.add_argument(
    'text',
    type=str,
    required=True,
    help="Body text is required"
)
weibo_post_parser.add_argument(
    'tags',
    type=str,
    action='append'
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
