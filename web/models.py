from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import datetime
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)
from web import config

db = SQLAlchemy()


# tags = db.Table(
#     'post_tags',
#     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
# )
#
# roles = db.Table(
#     'role_users',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
# )


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    expires_in = db.Column(db.DATETIME())
    openid = db.Column(db.String(255), unique=True)
    third_session = db.Column(db.String(255))
    session_key = db.Column(db.String(255))
    manager = db.Column(db.BOOLEAN(), default=False)  # 是否管理员
    can_send_weibo = db.Column(db.BOOLEAN(), default=True)  # 能否发布微博

    def __repr__(self):
        return '<User {}>'.format(self.openid)

    def get_id(self):
        return self.id

    @classmethod
    def get(cls, openid):
        user = cls.query.filter_by(openid=openid).first()
        if not user:
            return None
        else:
            return user

    @classmethod
    def gen_3rdsession(cls, value, expires_in=None):
        # 用OpenId加密生成3rdsession
        if not expires_in:
            expires_in = current_app.config['TOKEN_EXPIRES']
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        third_session = s.dumps(value)
        return third_session

    @classmethod
    def verify_auth_3rdsession(cls, thirdsession):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(thirdsession)
        except SignatureExpired:
            return False, {'status': 'fail', 'error': '认证已过期'}
        except BadSignature:
            return False, {'status': 'fail', 'error': 'session无效'}
        print(data)
        user = cls.get_user(data['openid'])
        return True, user

    @classmethod
    def refresh_3rdsession(cls, thirdsession):
        flag, user = cls.verify_auth_3rdsession(thirdsession=thirdsession)
        if not flag:
            return False, user
        value = {'openid': user.openid, 'session_key': user.session_key, 'expires_in': user.expires_in}
        third_session = cls.User.gen_3rdsession(value=value).decode('utf-8')
        user.third_session = third_session
        db.session.add(user)
        db.session.commit()
        return True, user

    @classmethod
    def get_manager_user_id(cls):
        user_list = cls.query.filter_by(manager=True)
        res = [user.openid for user in user_list]
        return res

    @classmethod
    def add(cls, expires_in, openid, third_session, session_key):
        user = cls.query.filter_by(openid=openid).first()
        if not user:
            user = cls()
            user.openid = openid
            print('新增用户 {}'.format(openid))
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(seconds=expires_in)
        user.expires_in = expires
        user.third_session = third_session
        user.session_key = session_key
        db.session.add(user)
        db.session.commit()
        return user


class Weixin_Gzh(db.Model):
    title_md5 = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    publish_time = db.Column(db.DATETIME())
    scrapy_time = db.Column(db.DATETIME())
    url = db.Column(db.String(300))
    html_content = db.Column(db.TEXT())
    content = db.Column(db.TEXT())
    cover = db.Column(db.String(300))
    digest = db.Column(db.String(300))
    gzh = db.Column(db.CHAR(50))
    success = db.Column(db.BOOLEAN(), default=False)

    @classmethod
    def to_dict(cls, m, detail=False):
        tmp = dict()
        tmp['id'] = m.title_md5
        tmp['title'] = m.title
        tmp['publish_time'] = m.publish_time
        tmp['url'] = m.url
        tmp['cover'] = m.cover
        tmp['digest'] = m.digest
        tmp['gzh'] = m.gzh
        if detail:
            tmp['content'] = m.content
            tmp['html_content'] = m.html_content
        return tmp

    @classmethod
    def to_list(cls, ms, detail=False):
        res = []
        for m in ms:
            res.append(cls.to_dict(m, detail))
        return res


class Weibo(db.Model):
    weibo_id = db.Column(db.String(50), primary_key=True)
    content = db.Column(db.String(300))
    img = db.Column(db.String(300))
    large_img = db.Column(db.String(300))
    likes = db.Column(db.Integer())
    comments = db.Column(db.Integer())
    reports = db.Column(db.Integer())
    weibo_name = db.Column(db.String(45))
    author = db.Column(db.String(100), nullable=True)
    publish_time = db.Column(db.DATETIME())
    mode = db.Column(db.CHAR(2))

    @classmethod
    def to_list(cls, ms, detail=False):
        res = []
        for m in ms:
            res.append(cls.to_dict(m, detail))
        return res

    @classmethod
    def to_dict(cls, m, detail=False):
        tmp = dict()
        tmp['id'] = m.weibo_id
        tmp['content'] = m.content
        tmp['img'] = m.img
        tmp['likes'] = m.likes
        tmp['comments'] = m.comments
        tmp['reports'] = m.reports
        tmp['weibo_name'] = m.weibo_name
        tmp['publish_time'] = m.publish_time
        # tmp['author'] = m.author
        if detail:
            if tmp['comments'] > 0:
                comments = Weibo_comment.query.filter_by(weibo=tmp['id'])
                tmp['comments'] = Weibo_comment.to_list(ms=comments)
        return tmp

    @classmethod
    def get(cls, weibo_id):
        weibo = cls.query.filter_by(weibo_id=weibo_id).first()
        if weibo:
            return weibo
        else:
            return None


class Weibo_comment(db.Model):
    comment_id = db.Column(db.String(50), primary_key=True)
    weibo = db.Column(db.String(50), db.ForeignKey('weibo.weibo_id'))
    comment = db.Column(db.String(200))
    publish_time = db.Column(db.DATETIME())
    author = db.Column(db.String(100))
    reply_author = db.Column(db.String(100), nullable=True)
    likes = db.Column(db.Integer())
    author_source = db.Column(db.BOOLEAN(), default=False)  # 是否本系统用户
    reply_author_source = db.Column(db.BOOLEAN(), default=False)  # 是否本系统用户
    weibo_obj = db.relationship('Weibo', backref=db.backref('comment_set', lazy='dynamic'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.comment[:15])

    @classmethod
    def to_list(cls, ms, detail=False):
        res = []
        for m in ms:
            res.append(cls.to_dict(m, detail))
        return res

    @classmethod
    def to_dict(cls, m, detail=False):
        tmp = dict()
        tmp['comment_id'] = m.comment_id
        tmp['weibo'] = m.weibo
        tmp['comment'] = m.comment
        tmp['publish_time'] = m.publish_time

        if m.author_source:
            name = config.UNNAMED
            author_id = m.author
        else:
            name = m.author
            author_id = None
        tmp['author'] = {
            "name": name,
            "id": author_id
        }
        if m.reply_author:
            if m.reply_author_source:
                tmp['reply_author'] = config.UNNAMED
            else:
                tmp['reply_author'] = m.reply_author
        tmp['likes'] = m.likes
        return tmp

    @classmethod
    def get(cls, comment_id):
        comment = cls.query.filter_by(comment_id=comment_id).first()
        if comment:
            return comment
        else:
            return None

    # 获取非本系统发的微博评论
    @classmethod
    def get_other_comment(cls, attr='comment_id'):
        res = cls.query.filter_by(author_source=False).filter(
            Weibo_comment.weibo_obj.has(Weibo.weibo_name == config.WEIBO_NAME))
        if attr:
            res = [getattr(o, attr) for o in res]
        return res


class Official(db.Model):
    article_id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.TEXT())
    html_content = db.Column(db.TEXT())
    publish_time = db.Column(db.DATE())
    url = db.Column(db.String(256))

    @classmethod
    def to_list(cls, ms, detail=False):
        res = []
        for m in ms:
            res.append(cls.to_dict(m, detail))
        return res

    @classmethod
    def to_dict(cls, m, detail=False):
        tmp = dict()
        tmp['article_id'] = m.article_id
        tmp['title'] = m.title
        tmp['publish_time'] = m.publish_time
        if detail:
            tmp['content'] = m.content
        return tmp


class Message(db.Model):
    message_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(100))
    content = db.Column(db.String(300))
    weibo_id = db.Column(db.String(100))
    create_time = db.Column(db.DATETIME())
    is_read = db.Column(db.BOOLEAN(), default=False)

    def __init__(self):
        self.create_time = datetime.datetime.now()

    @classmethod
    def list(cls, user_id, page, not_read=True):
        ms = cls().query.filter_by(user_id=user_id)
        if not_read:
            ms = ms.filter_by(is_read=False)
        ms = ms.order_by(
            Message.create_time.desc()
        ).paginate(page, 30).items
        if not_read:
            for m in ms:
                m.is_read = True
                db.session.add(m)
            db.session.commit()
        return ms

    @classmethod
    def to_dict(cls, m, detail=False):
        tmp = dict()
        tmp['weibo_id'] = m.weibo_id
        tmp['content'] = m.content
        tmp['create_time'] = m.create_time
        tmp['is_read'] = m.is_read
        tmp['message_id'] = m.message_id
        return tmp

    @classmethod
    def to_list(cls, ms, detail=False):
        res = []
        for m in ms:
            res.append(cls.to_dict(m, detail))
        return res

    @classmethod
    def add(cls, weibo, user_id, content):
        if not isinstance(user_id, list):
            user_id = [user_id]
        for user in user_id:
            msg = cls()
            msg.weibo_id = weibo.weibo_id
            msg.user_id = user
            msg.content = content
            db.session.add(msg)
            db.session.commit()
            return msg

    @classmethod
    def new_msg_count(cls, user_id):
        return cls().query.filter_by(is_read=False, user_id=user_id).count()

# class Role(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return '<Role {}>'.format(self.name)
#
#
# class Post(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(255))
#     text = db.Column(db.Text())
#     publish_date = db.Column(db.DateTime())
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
#     comments = db.relationship(
#         'Comment',
#         backref='post',
#         lazy='dynamic'
#     )
#     tags = db.relationship(
#         'Tag',
#         secondary=tags,
#         backref=db.backref('posts', lazy='dynamic')
#     )
#
#     def __init__(self, title):
#         self.title = title
#
#     def __repr__(self):
#         return "<Post '{}'>".format(self.title)
#
#
# class Comment(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(255))
#     text = db.Column(db.Text())
#     date = db.Column(db.DateTime())
#     post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
#
#     def __repr__(self):
#         return "<Comment '{}'>".format(self.text[:15])
#
#
# class Tag(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(255))
#
#     def __init__(self, title):
#         self.title = title
#
#     def __repr__(self):
#         return "<Tag '{}'>".format(self.title)
#
#
# class Reminder(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     date = db.Column(db.DateTime())
#     email = db.Column(db.String())
#     text = db.Column(db.Text())
#
#     def __repr__(self):
#         return "<Reminder '{}'>".format(self.text[:20])
