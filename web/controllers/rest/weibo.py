from flask import abort, jsonify, request, session
from flask_restful import Resource
from web.tasks import send_weibo, send_weibo_comment
from web.models import db, Weibo, User, Message, Weibo_to_delete, Tag
from web import config
from .parsers import (
    weibo_get_parser,
    weibo_post_parser,
    weibo_comment_post_parser,
    weibo_delete_parser
)
from web.extensions import cache
from weibo_nlp.nlp import best_word_feature, d
import os, pickle, jieba


@cache.cached(timeout=300, key_prefix='classifier')
def get_classifier():
    f = open(os.path.join(d, 'best_word.pickle'), 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


@cache.cached(timeout=300, key_prefix='feature')
def get_feature():
    return best_word_feature


def get_sentiment(content):
    classifier = get_classifier()
    feature = get_feature()
    item = feature(jieba.cut(content, cut_all=False))
    sent1 = classifier.prob_classify(item)
    prob = sent1._prob_dict
    print(prob)
    if abs(prob['neg'] - prob['pos'] < 1):
        return 2
    elif sent1.max() == 'neg':
        return 1
    elif sent1.max() == 'pos':
        return 0
    return 2


class Weibo_Api(Resource):
    def get(self, weibo_id=None):
        color_level = 0
        is_authorization = session.get('is_authorization')
        openid = None
        if is_authorization:
            openid = session.get('user_id', None)
            user = User.get(openid=openid)
            if user:
                color_level = user.get_color_level()
        color_dict = config.color_level_dict[color_level]
        args = weibo_get_parser.parse_args()
        page = args['page'] or 1
        tag = args['tag'] or None
        if weibo_id:
            if weibo_id == 'self':
                if not is_authorization:
                    return abort(401, {"msg": session.get('error')})
                post = Weibo.query.filter(Weibo.status.isnot(True)).filter(Weibo.author == openid).order_by(
                    Weibo.publish_time.desc()
                ).paginate(page, 30)
                weibo_list = Weibo.to_list(ms=post.items, detail=False)
                res = {
                    "pages": post.pages,
                    "total": post.total,
                    "now_page": page,
                    "weibo": weibo_list,
                }
                res.update(color_dict)
                return jsonify(res)
            else:
                post = Weibo.query.filter(Weibo.status.isnot(True)).filter_by(weibo_id=weibo_id).first()
                if not post:
                    abort(404, {'error': '不存在此id的微博'})
                return jsonify(Weibo.to_dict(post, detail=True, openid=openid))
        else:
            if tag:
                posts = Weibo.query.filter(Weibo.tags.any(Tag.name == tag))
            else:
                posts = Weibo.query
            posts = posts.filter(Weibo.status.isnot(True)).order_by(
                Weibo.publish_time.desc()
            ).paginate(page, 30)
            msg_count = Message.new_msg_count(user_id=session.get('user_id', ''))
            weibo_list = Weibo.to_list(ms=posts.items, detail=False)
            res = {
                "pages": posts.pages,
                "total": posts.total,
                "now_page": page,
                "msg_count": msg_count,
                "weibo": weibo_list,
            }
            res.update(color_dict)
            return jsonify(res)

    def post(self):
        request_path = request.path
        path_list = request_path.split('/')
        if 'comment' in path_list[-1]:
            args = weibo_comment_post_parser.parse_args(strict=True)
        else:
            args = weibo_post_parser.parse_args(strict=True)
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"msg": session.get('error')})
        user = User.get(openid=session.get('user_id'))
        if path_list[-1] == 'comment':
            content = args['content']
            weibo_id = args['weibo_id']
            reply_author = args.get('reply_author_name', None)
            reply_author_id = args.get('reply_author_id', None)
            reply_comment_id = args.get('reply_comment_id', None)
            send_weibo_comment.apply_async(
                kwargs={'user_id': user.openid, 'content': content, 'weibo_id': weibo_id, 'reply_author': reply_author,
                        'reply_author_id': reply_author_id, 'reply_comment_id': reply_comment_id})
            # send_weibo_comment(user=user,content=content,weibo_id=weibo_id,reply_author=reply_author,reply_comment_id=reply_comment_id,reply_author_id=reply_author_id)
            return jsonify({'msg': 'success'})

        else:
            if user.is_over_post():
                return abort(400, {"msg": "你发送微博过于频繁,请稍后再发"})

            content = args['content']
            if len(content) > 140:
                return abort(400, {"msg": "字数超过140个"})
            if len(content.strip()) <= 0:
                return abort(400, {"msg": "内容不合法"})
            tag_id = args.get('tags', None)
            msg = '发送成功,谢谢使用'
            mode = 2
            try:
                if not tag_id:
                    mode = get_sentiment(content=content)
                    user.set_color_level(mode)
                    if mode == 1:
                        is_neg = Weibo.analysis_sentiment(user_id=user.openid, weibo_mode=mode)
                        if is_neg:
                            msg = '发成功了。希望好运气降临你身边'

                file = args.get('file', None)
                if file:
                    file = os.path.join(config.UPLOAD_PATH, file)
                send_weibo.apply_async(
                    kwargs={'user_id': user.openid, 'mode': mode, 'content': content, 'file': file, 'tag_id': tag_id})
                # send_weibo(user=user,content=content,file=file)
                return jsonify({'msg': msg})
            except Exception as e:
                return abort(500, {'msg', str(e)})

    def delete(self):
        is_authorization = session.get('is_authorization')
        if not is_authorization:
            return abort(401, {"error": session.get('error')})
        user_id = session.get('user_id')
        args = weibo_delete_parser.parse_args(strict=True)
        weibo_id = args['weibo_id']
        weibo = Weibo.query.filter_by(weibo_id=weibo_id).first()
        if not weibo:
            return abort(400, {'error': '无此微博'})
        if weibo.author != user_id:
            return abort(403, {'error': '此微博作者不是本人, 不能删除'})
        weibo.status = True
        db.session.add(weibo)

        weibo_delete = Weibo_to_delete()
        weibo_delete.reason = Weibo_to_delete.Self_apply
        weibo_delete.weibo_id = weibo_id
        weibo_delete.done = False
        db.session.add(weibo_delete)
        db.session.commit()

        Message.add(weibo=None, user_id=User.get_manager_user_id(),
                    content=config.WEIBO_APPLY_DELETE_MSG.format(content=weibo.content, id=weibo_id))

        from qyweixin.qyweixin_api import send_weixin_message, qyweixin_text_type
        send_weixin_message(send_type=qyweixin_text_type,
                            msg_content=config.WEIBO_APPLY_DELETE_MSG.format(content=weibo.content, id=weibo_id))

        from elasticsearch_tool.init_models import Weibo as ES_Weibo
        weibo = ES_Weibo.get(id=weibo_id)
        weibo.delete()
        return jsonify({'msg': '删除申请成功,微博将在今天内删除'})
