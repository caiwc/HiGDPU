from web.weibo_api import post_weibo, post_weibo_commet, reply_comment, get_comment_to_me
from web.extensions import celery
from weixin_scrapy.verifycode import handel_verifycode
from web.models import db, User, Weibo, Weibo_comment, Message, Tag
from web import config
from weixin_scrapy.main import run
import datetime
from web.utils import str_md5, weibo_time_format
from elasticsearch_tool.init_models import get_suggests, Weibo as ES_Weibo


@celery.task()
def log(msg):
    return msg


@celery.task()
def multiply(x, y):
    a = x * y
    print(a)
    return a


@celery.task(ignore_result=True, time_limit=300)
def verifycode_handle(url, operation):
    handel_verifycode(url=url, operation=operation, by_qyweixin=True)
    return True


@celery.task()
def send_weibo(user_id, content, mode, file=None):
    from web.utils import weibo_time_format
    user = User.get(openid=user_id)
    res = post_weibo(content=content, files_path=file)
    print(res)
    if res:
        weibo = Weibo()
        weibo.content = content
        created_time = weibo_time_format(res['created_at'])
        weibo.publish_time = created_time
        weibo.img = res.get('thumbnail_pic', '')
        weibo.large_img = res.get('original_pic', '')
        weibo.weibo_id = res['id']
        weibo.weibo_name = res['user']['domain']
        weibo.likes = 0
        weibo.reports = 0
        weibo.author = user.openid
        weibo.mode = mode
        db.session.add(weibo)
        db.session.commit()

        es_weibo = ES_Weibo()
        es_weibo._id = res['id']
        es_weibo.content = content
        es_weibo.publish_time = created_time
        es_weibo.comment = 0
        es_weibo.suggest = get_suggests(ES_Weibo._doc_type.index, [(weibo.content, 10)], ES_Weibo)
        es_weibo.save()

        if file:
            import os
            os.remove(file)


@celery.task(
    default_retry_delay=300,
    max_retries=5
)
def send_weibo_comment(user_id, weibo_id, content, reply_author=None, reply_author_id=None, reply_comment_id=None):
    from web.utils import weibo_time_format
    user = User.get(openid=user_id)
    weibo = Weibo.query.filter_by(weibo_id=weibo_id).first()
    if weibo:
        comment = Weibo_comment()
        if reply_comment_id:
            if reply_author_id:
                comment.reply_author = reply_author_id
                comment.reply_author_source = True
            else:
                comment.reply_author = reply_author
                comment.reply_author_source = False
        if weibo.weibo_name == config.WEIBO_NAME:
            try:
                if not reply_author:
                    res = post_weibo_commet(weibo_id=weibo_id, comment=content)
                else:
                    res = reply_comment(weibo_id=weibo_id, comment_id=reply_comment_id, comment=content)
            except Exception as e:
                print(e)
                return False
            comment.publish_time = weibo_time_format(res['created_at'])
            comment.comment_id = res['id']
        else:
            comment.comment_id = str_md5(weibo_id + content)
            comment.publish_time = datetime.datetime.now()
        comment.weibo = weibo_id
        comment.comment = content
        comment.author = user.openid
        comment.likes = 0
        comment.author_source = True
        db.session.add(comment)
        db.session.commit()
        if weibo.author:
            Message.add(weibo=weibo, user_id=weibo.author, content=config.WEIBO_COMMENT_MSG)
        if reply_comment_id and reply_author_id:
            Message.add(weibo=weibo, user_id=reply_author, content=config.WEIBO_REPLY_MSG)

        ES_Weibo.add_comment(weibo_id=weibo_id)
        return True
    else:
        return False


@celery.task(ignore_result=True)
def crawl(operation):
    run(spider=operation)


@celery.task(
    name="web.tasks.get_comment_message",
    ignore_result=True,
    default_retry_delay=30,
    max_retries=3
)
def get_comment_message():
    qyweixin_msg = "定时任务反馈: "
    try:
        res = get_comment_to_me()
        comment_list = res.get('comments', [])
        record = []
        old_comment_id_set = set(Weibo_comment.get_other_comment('comment_id'))

        for msg in comment_list:
            comment_id = msg['idstr']
            old_comment_id_set.discard(comment_id)
            comment = Weibo_comment.get(comment_id=comment_id)
            if not comment:
                weibo_id = msg['status']['idstr']
                print("update weibo " + weibo_id)
                weibo = Weibo.get(weibo_id=weibo_id)

                comment = Weibo_comment()
                comment.weibo = weibo.weibo_id
                comment.comment_id = comment_id
                comment.author = msg['user']['name']
                comment.author_source = False
                comment.publish_time = weibo_time_format(msg['created_at'])
                if 'reply_original_text' in msg:
                    comment.comment = msg['reply_original_text']
                    if msg['reply_comment']['user']['name'] == config.WEIBO_NAME:
                        reply_comment_id = msg['reply_comment']['idstr']
                        reply_comment = Weibo_comment.get(reply_comment_id)
                        if reply_comment:
                            comment.reply_author = reply_comment.author
                            comment.reply_author_source = True
                            Message.add(weibo=weibo, user_id=reply_comment.author, content=config.WEIBO_REPLY_MSG)
                    else:
                        comment.reply_author = msg['reply_comment']['user']['name']
                        comment.reply_author_source = False
                else:
                    comment.comment = msg['text']
                if weibo:
                    Message.add(weibo=weibo, user_id=weibo.author, content=config.WEIBO_COMMENT_MSG)
                log_msg = "save comment object {1}({0})".format(comment.comment_id, comment.comment)

                ES_Weibo.add_comment(weibo_id=weibo_id)

            else:
                log_msg = "update comment object {1}({0})".format(comment.comment_id, comment.comment)

            record.append(log_msg)
            print(log_msg)
            comment.likes = msg['like_count']
            db.session.add(comment)

        for delete_id in old_comment_id_set:
            comment = Weibo_comment.get(comment_id=delete_id)
            if comment:
                db.session.delete(comment)

            ES_Weibo.add_comment(weibo_id=delete_id, add=False)

            log_msg = "delete comment object {1}({0})".format(comment.comment_id, comment.comment)
            record.append(log_msg)
        db.session.commit()
        qyweixin_msg = qyweixin_msg + ";".join(record)
    except Exception as e:
        qyweixin_msg = qyweixin_msg + 'ERROR: ' + str(e)
        print(qyweixin_msg)
    finally:
        from qyweixin.qyweixin_api import send_weixin_message, qyweixin_text_type
        send_weixin_message(send_type=qyweixin_text_type, msg_content=qyweixin_msg)


@celery.task(
    name="web.tasks.add_weibo_tags"
)
def add_weibo_tags():
    weibo_list = Weibo.query.filter(~Weibo.tags.any()).order_by(Weibo.publish_time.desc()).paginate(1, 100).items
    for weibo in weibo_list:
        if not weibo.tags:
            if '中山' in weibo.content or '大山' in weibo.content:
                weibo.add_tags(1)
                print('{} add tag `{}`'.format(weibo.content, '中山'))
            elif '大学城' in weibo.content:
                weibo.add_tags(4)
                print('{} add tag `{}`'.format(weibo.content, '大学城'))


@celery.task(
    default_retry_delay=20,
    max_retries=3
)
def delete_weibo():
    from web.models import Weibo_to_delete
    weibo_list = Weibo_to_delete.query.filter(done=False)


@celery.task(
    name="web.tasks.weibo_report"
)
def weibo_report():
    from weibo_nlp.word_cloud import get_word_cloud
    from weibo_nlp.weibo_count import zs_dxc_count, daily_weibo_count, recently_weibo_count
    from sqlalchemy import extract, and_
    today = datetime.date.today()
    weibo_list = Weibo.query.filter(and_(
        extract('year', Weibo.publish_time) == today.year,
        extract('month', Weibo.publish_time) == today.month - 1))
    get_word_cloud([o.content for o in weibo_list.all()])
    zs_dxc_count(weibo_query=weibo_list)
    daily_weibo_count(weibo_query=weibo_list)
    recently_weibo_count(6)


class ReportData():
    def __init__(self):
        self.title = ""
        self.date = None
        self.count = 0

