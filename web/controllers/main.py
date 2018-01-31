from flask import (current_app,
                   Blueprint,
                   redirect,
                   url_for,
                   request,
                   jsonify,
                   make_response,
                   flash,
                   session)
from web import config
import requests
import json
import redis
from web import utils
from flask_restful import reqparse
from web.models import db
from qyweixin.WXBizMsgCrypt import WXBizMsgCrypt

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


@main_blueprint.route('/')
def index():
    return redirect(url_for('weibo_api'))


@main_blueprint.route('/api/authorization', methods=['POST'])
def authorization():
    url = config.WEIXIN_AUTH_URL
    headers = {"content-type": "application/json"}
    js_code = request.json['code']
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


@main_blueprint.route('/api/qyweixin', methods=['GET', 'POST'])
def qyweixin_authorization():
    import xml.etree.cElementTree as ET
    arg = request.args
    sVerifyMsgSig = arg['msg_signature']
    sVerifyTimeStamp = arg['timestamp']
    sVerifyNonce = arg['nonce']
    wxcpt = WXBizMsgCrypt(config.Token, config.EncodingAESKey, config.CORPID)
    if request.method == 'GET':
        sVerifyEchoStr = arg['echostr']
        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        if (ret != 0):
            raise ValueError("ERR: VerifyURL ret: " + str(ret))
        return sEchoStr.decode('utf-8')
    if request.method == 'POST':
        sReqData = request.data
        ret, sMsg = wxcpt.DecryptMsg(sReqData, sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce)
        if (ret != 0):
            raise ValueError("ERR: VerifyURL ret: " + str(ret))
        xml_tree = ET.fromstring(sMsg)
        print(sMsg)
        msg_type = xml_tree.find("MsgType").text
        from_user = xml_tree.find('ToUserName').text
        to_user = xml_tree.find('FromUserName').text
        if 'text' in msg_type:
            content = xml_tree.find("Content").text
            if content == config.QYWEIXIN_VERIFYCODE:
                res = utils.msg_encrp(wxcpt=wxcpt, to_user=from_user, from_user=to_user, content='\xe8\xaf\x86\xe5\x88\xab\xe9\xaa\x8c\xe8\xaf\x81\xe7\xa0\x81',
                                      sReqNonce=sVerifyNonce)
                print(res)
                response = make_response(res)
                response.content_type = 'application/xml'
                return response
            else:
                res = utils.msg_encrp(wxcpt=wxcpt, to_user=to_user, from_user=from_user, content='url',
                                      sReqNonce=sVerifyNonce)
                return res
        if 'event' in msg_type:
            event_key = xml_tree.find("EventKey").text
            print(event_key)
            if event_key == 'verifycode':
                from weixin_scrapy.verifycode import handel_verifycode
                res = utils.msg_encrp(wxcpt=wxcpt, to_user=to_user, from_user=from_user, content='url',
                                      sReqNonce=sVerifyNonce)
                print(res)
                response = make_response(res)
                response.content_type = 'application/xml'
                return response

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
