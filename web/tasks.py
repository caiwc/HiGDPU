import smtplib
import datetime
from email.mime.text import MIMEText
from flask import render_template
from web.weibo_api import post_weibo
from web.extensions import celery
from weixin_scrapy.verifycode import handel_verifycode
from web.models import db, User, Weibo
from weixin_scrapy.main import run


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
def send_weibo(content, file=None):
    from web.utils import weibo_time_format
    res = post_weibo(content=content, files_path=file)
    print(res)
    if res:
        weibo = Weibo()
        weibo.content = content
        created_time = weibo_time_format(res['created_at'])
        pic_list = res['pic_urls']
        pic = pic_list[0] if pic_list else ''
        weibo.publish_time = created_time
        weibo.img = pic
        weibo.weibo_id = res['id']
        weibo.weibo_name = res['user']['domain']
        weibo.likes = 0
        weibo.reports = 0
        weibo.comments = 0
        db.session.add(weibo)
        db.session.commit()


@celery.task(ignore_result=True)
def crawl(operation):
    run(spider=operation)

# @celery.task()
# def add_user(username, third_session, expires_in, session_key, openid_id):
#     user = User.query.filter_by(openid_id=openid_id).first()
#     if not user:
#         user = User()
#         user.username = username
#         now = datetime.datetime.now()
#         expires = now+datetime.timedelta(seconds=expires_in)
#         user.expires_in = expires
#         user.third_session = third_session
#         user.openid_id = openid_id
#         user.session_key = session_key
#         db.session.add(user)
#         db.session.commit()
#         print('新增用户 {}'.format(username))
#     return user.id

# @celery.task(
#     bind=True,
#     ignore_result=True,
#     default_retry_delay=300,
#     max_retries=5
# )
# def remind(self, pk):
#     reminder = Reminder.query.get(pk)
#     msg = MIMEText(reminder.text)
#
#     msg['Subject'] = "Your reminder"
#     msg['From'] = ""
#     msg['To'] = reminder.email
#
#     try:
#         smtp_server = smtplib.SMTP('localhost')
#         smtp_server.starttls()
#         # smtp_server.login(user, password)
#         smtp_server.sendmail("", [reminder.email], msg.as_string())
#         smtp_server.close()
#
#         return
#     except Exception, e:
#         self.retry(exc=e)
#
#
# @celery.task(
#     bind=True,
#     ignore_result=True,
#     default_retry_delay=300,
#     max_retries=5
# )
# def digest(self):
#     # find the start and end of this week
#     year, week = datetime.datetime.now().isocalendar()[0:2]
#     date = datetime.date(year, 1, 1)
#     if (date.weekday() > 3):
#         date = date + datetime.timedelta(7 - date.weekday())
#     else:
#         date = date - datetime.timedelta(date.weekday())
#     delta = datetime.timedelta(days=(week - 1) * 7)
#     start, end = date + delta, date + delta + datetime.timedelta(days=6)
#
#     posts = Post.query.filter(
#         Post.publish_date >= start,
#         Post.publish_date <= end
#     ).all()
#
#     if (len(posts) == 0):
#         return
#
#     msg = MIMEText(render_template("digest.html", posts=posts), 'html')
#
#     msg['Subject'] = "Weekly Digest"
#     msg['From'] = ""
#
#     try:
#         smtp_server = smtplib.SMTP('localhost')
#         smtp_server.starttls()
#         # smtp_server.login(user, password)
#         smtp_server.sendmail("", [""], msg.as_string())
#         smtp_server.close()
#
#         return
#     except Exception, e:
#         self.retry(exc=e)
#
#
# def on_reminder_save(mapper, connect, self):
#     remind.apply_async(args=(self.id,), eta=self.date)
