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
    express_in = db.Column(db.DATETIME())
    openid_id = db.Column(db.String(255))
    thrid_session = db.Column(db.String(255))
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

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.get(data['id'])
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
