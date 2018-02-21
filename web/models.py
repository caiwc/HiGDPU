from flask import current_app
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.login import AnonymousUserMixin
import datetime
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)

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
    username = db.Column(db.String(255))
    expires_in = db.Column(db.DATETIME())
    openid = db.Column(db.String(255))
    third_session = db.Column(db.String(255))
    session_key = db.Column(db.String(255))

    #     roles = db.relationship(
    #         'Role',
    #         secondary=roles,
    #         backref=db.backref('users', lazy='dynamic')
    #     )
    #

    # def __init__(self, username):
    #     self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def is_express(self):
        if self.express_in < datetime.datetime.now():
            return False
        return True

    def get_id(self):
        return self.id

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
            return False, {'status': 'fail', 'data': {'msg': 'expired token'}}
        except BadSignature:
            return False, {'status': 'fail', 'data': {'msg': 'useless token'}}
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
    def get_user(cls, openid):
        user = cls.query.filter_by(openid=openid).first()
        if not user:
            raise ValueError('不存在当前用户')
        return user

    @classmethod
    def add(cls, username, expires_in, openid, third_session, session_key):
        user = cls.query.filter_by(openid=openid).first()
        if not user:
            user = cls()
            user.openid = openid
            print('新增用户 {}'.format(username))
        user.username = username
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(seconds=expires_in)
        user.expires_in = expires
        user.third_session = third_session
        user.session_key = session_key
        db.session.add(user)
        db.session.commit()
        return user.id


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


class Weibo(db.Model):
    weibo_id = db.Column(db.String(50), primary_key=True)
    content = db.Column(db.String(300))
    img = db.Column(db.String(300))
    likes = db.Column(db.Integer())
    comments = db.Column(db.Integer())
    reports = db.Column(db.Integer())
    weibo_name = db.Column(db.String(45))
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    publish_time = db.Column(db.DATETIME())

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
        tmp['author_id'] = m.author_id
        if detail:
            pass
        return tmp

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
