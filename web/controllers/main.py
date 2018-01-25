from flask import (current_app,
                   Blueprint,
                   redirect,
                   url_for,
                   request,
                   jsonify,
                   flash,
                   session)
from web import config
import requests
import json
from web import utils
from flask_restful import reqparse
from web.models import db
# from flask.ext.principal import (
#     Identity,
#     AnonymousIdentity,
#     identity_changed
# )

# from web.extensions import oid, facebook, twitter

main_blueprint = Blueprint(
    'main',
    __name__,
)

authorization_post_parser = reqparse.RequestParser()
authorization_post_parser.add_argument(
    'code',
    type=str,
    required=True,
    help="js code to get authorization"
)
authorization_post_parser.add_argument(
    'username',
    type='str',
    required=True,
    help="user weixin name"
)

@main_blueprint.route('/')
def index():
    return redirect(url_for('weibo_api'))


@main_blueprint.route('/api/authorization', methods=['POST'])
def authorization():
    url = config.WEIXIN_AUTH_URL
    headers = {"content-type": "application/json"}
    args = authorization_post_parser.parse_args(strict=True)
    js_code = args['code']
    username = args['username']
    res = requests.get(url=url.format(JSCODE=js_code), headers=headers)
    if res.status_code == 200:
        res_json = res.json()
        if 'session_key' in res_json:
            openId = res_json['openid']
            secret_value = {
                'openid': openId,
                'session_key': res_json['session_key']
            }
            expires_in = res_json['expires_in']
            thrid_session = utils.gen_3rdsession({'openId': openId}).decode('utf-8')
            print(thrid_session)
            secret_value = json.dumps(secret_value)
            return jsonify({thrid_session: secret_value})
        elif 'errcode' in res_json:
            return res_json['errmsg']
    return 'request error'

# @main_blueprint.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     form = LoginForm()
#     openid_form = OpenIDForm()
#
#     if openid_form.validate_on_submit():
#         return oid.try_login(
#             openid_form.openid.data,
#             ask_for=['nickname', 'email'],
#             ask_for_optional=['fullname']
#         )
#
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).one()
#         login_user(user, remember=form.remember.data)
#
#         identity_changed.send(
#             current_app._get_current_object(),
#             identity=Identity(user.id)
#         )
#
#         flash("You have been logged in.", category="success")
#         return redirect(url_for('blog.home'))
#
#     openid_errors = oid.fetch_error()
#     if openid_errors:
#         flash(openid_errors, category="danger")
#
#     return render_template('login.html', form=form, openid_form=openid_form)
#
#
# @main_blueprint.route('/facebook')
# def facebook_login():
#     return facebook.authorize(
#         callback=url_for(
#             '.facebook_authorized',
#             next=request.referrer or None,
#             _external=True
#         )
#     )
#
#
# @main_blueprint.route('/facebook/authorized')
# @facebook.authorized_handler
# def facebook_authorized(resp):
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#
#     session['facebook_oauth_token'] = (resp['access_token'], '')
#
#     me = facebook.get('/me')
#     user = User.query.filter_by(
#         username=me.data['first_name'] + " " + me.data['last_name']
#     ).first()
#
#     if not user:
#         user = User(me.data['first_name'] + " " + me.data['last_name'])
#         db.session.add(user)
#         db.session.commit()
#
#     login_user(user)
#     flash("You have been logged in.", category="success")
#
#     return redirect(request.args.get('next') or url_for('blog.home'))
#
#
# @main_blueprint.route('/twitter-login')
# def twitter_login():
#     return twitter.authorize(
#         callback=url_for(
#             '.twitter_authorized',
#             next=request.referrer or None,
#             _external=True
#         )
#     )
#
#
# @main_blueprint.route('/twitter-login/authorized')
# @twitter.authorized_handler
# def twitter_authorized(resp):
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#
#     session['twitter_oauth_token'] = resp['oauth_token'] + \
#         resp['oauth_token_secret']
#
#     user = User.query.filter_by(username=resp['screen_name']).first()
#     if not user:
#         user = User(resp['screen_name'], '')
#         db.session.add(user)
#         db.session.commit()
#
#     login_user(user)
#     flash("You have been logged in.", category="success")
#
#     return redirect(request.args.get('next') or url_for('blog.home'))
#
#
# @main_blueprint.route('/logout', methods=['GET', 'POST'])
# def logout():
#     logout_user()
#
#     identity_changed.send(
#         current_app._get_current_object(),
#         identity=AnonymousIdentity()
#     )
#
#     flash("You have been logged out.", category="success")
#     return redirect(url_for('.login'))
