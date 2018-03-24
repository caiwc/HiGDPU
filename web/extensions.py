from flask import flash, redirect, request, session
from web.models import User
from flask_restful import Api
from flask_celery import Celery
from flask_cache import Cache
from werkzeug.datastructures import Headers
from flask import Response
from web.config import TOKEN_KEY, DevConfig

celery = Celery()
cache = Cache(config=DevConfig.REDIS)
rest_api = Api()


class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')
        # 跨域控制
        origin = ('Access-Control-Allow-Origin', '*')
        methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        if headers:
            headers.add(*origin)
            headers.add(*methods)
        else:
            headers = Headers([origin, methods])
        kwargs['headers'] = headers
        super().__init__(response, **kwargs)


def get_opt_user():
    third_session = request.headers.get(TOKEN_KEY, None)
    if not third_session:
        session['is_authorization'] = False
        session['error'] = '无third_session'
    else:
        flag, data = User.verify_auth_3rdsession(thirdsession=third_session)
        if not flag:
            session['is_authorization'] = False
            session['error'] = data['error']
        else:
            user_id = data.openid
            session['user_id'] = user_id
            session['is_authorization'] = True
    return

# admin_permission = Permission(RoleNeed('admin'))
# poster_permission = Permission(RoleNeed('poster'))
# default_permission = Permission(RoleNeed('default'))
#
#
# login_manager = LoginManager()
# login_manager.login_view = "main.login"
# login_manager.session_protection = "strong"
# login_manager.login_message = "Please login to access this page"
# login_manager.login_message_category = "info"




# @login_manager.user_loader
# def load_user(userid):
#     from models import User
#     return User.query.get(userid)
#
#
# @oid.after_login
# def create_or_login(resp):
#     from models import db, User
#     username = resp.fullname or resp.nickname or resp.email
#
#     if not username:
#         flash('Invalid login. Please try again.', 'danger')
#         return redirect(url_for('main.login'))
#
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         user = User(username)
#         db.session.add(user)
#         db.session.commit()
#
#     session['username'] = username
#     return redirect(url_for('blog.home'))
#
#
# facebook = oauth.remote_app(
#     'facebook',
#     base_url='https://graph.facebook.com/',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     authorize_url='https://www.facebook.com/dialog/oauth',
#     consumer_key='',
#     consumer_secret='',
#     request_token_params={'scope': 'email'}
# )
#
# twitter = oauth.remote_app(
#     'twitter',
#     base_url='https://api.twitter.com/1.1/',
#     request_token_url='https://api.twitter.com/oauth/request_token',
#     access_token_url='https://api.twitter.com/oauth/access_token',
#     authorize_url='https://api.twitter.com/oauth/authenticate',
#     consumer_key='',
#     consumer_secret=''
# )
#
#
# @facebook.tokengetter
# def get_facebook_oauth_token():
#     return session.get('facebook_oauth_token')
#
#
# @twitter.tokengetter
# def get_twitter_oauth_token():
#     return session.get('twitter_oauth_token')
