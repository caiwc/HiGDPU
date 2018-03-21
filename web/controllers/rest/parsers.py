from flask_restful import reqparse

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)

search_post_parser = reqparse.RequestParser()
search_post_parser.add_argument('page', type=int, required=False)
search_post_parser.add_argument('type', type=str, required=False)
search_post_parser.add_argument('order', type=str, required=False)
search_post_parser.add_argument('query', type=str, required=True)

official_get_parser = reqparse.RequestParser()
official_get_parser.add_argument('page', type=int, location=['args'])

message_get_parser = reqparse.RequestParser()
message_get_parser.add_argument('page', type=int, location=['args'])
message_get_parser.add_argument('not_read', type=str, location=['args'])

manage_post_parser = reqparse.RequestParser()
manage_post_parser.add_argument(
    'weibo_id',
    type=str,
    required=True,
    help="weibo id"
)
manage_post_parser.add_argument(
    'reason',
    type=str,
    required=True,
    help="删除微博原因"

)

weibo_get_parser = reqparse.RequestParser()
weibo_get_parser.add_argument('page', type=int, location=['args'])
weibo_get_parser.add_argument('tag', type=str, location=['args'])

weixin_get_parser = reqparse.RequestParser()
weixin_get_parser.add_argument('page', type=int, location=['args'])
weixin_get_parser.add_argument('gzh', type=str, location=['args'])

authorization_post_parser = reqparse.RequestParser()
authorization_post_parser.add_argument('code', type=str, required=True)

weibo_post_parser = reqparse.RequestParser()
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

weibo_comment_post_parser = reqparse.RequestParser()
weibo_comment_post_parser.add_argument(
    'weibo_id',
    type=str,
    required=True
)
weibo_comment_post_parser.add_argument(
    'content',
    type=str,
    required=True
)
weibo_comment_post_parser.add_argument(
    'reply_author_name',
    type=str,
    required=False
)
weibo_comment_post_parser.add_argument(
    'reply_author_id',
    type=str,
    required=False
)
weibo_comment_post_parser.add_argument(
    'reply_comment_id',
    type=str,
    required=False
)

weibo_delete_parser = reqparse.RequestParser()
weibo_delete_parser.add_argument(
    'weibo_id',
    type=str,
    required=True
)
