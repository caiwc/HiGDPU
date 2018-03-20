from flask import (current_app,
                   Blueprint,
                   request,
                   jsonify,
                   make_response,
                   g,
                   flash,
                   session)
from web import config
import os
import redis
from web.controllers import api_tool
from web.models import db, User
from qyweixin.WXBizMsgCrypt import WXBizMsgCrypt
from web.tasks import verifycode_handle, crawl

main_blueprint = Blueprint(
    'main',
    __name__,
)

can_commit = 'can_commit'
wxcpt = None


@main_blueprint.route('/api/handsome')
def index():
    return """
    城哥最帅
    城哥真的真的很帅"""


@main_blueprint.route('/api/upload', methods=['POST'])
def upload_file():
    is_authorization = session.get('is_authorization')
    if not is_authorization:
        return jsonify({"error": session.get('error')}), 401
    from web.utils import gen_filename
    if 'file' not in request.files:
        return jsonify({'error': '未获取到文件'}), 400
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': '仅支持JPEG、GIF、PNG图片'}), 400
    filename = gen_filename(file.filename)
    if not os.path.exists(config.UPLOAD_PATH):
        os.mkdir(config.UPLOAD_PATH)
    file.save(os.path.join(config.UPLOAD_PATH, filename))
    return jsonify({'filename': filename}), 200


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main_blueprint.route('/api/qyweixin', methods=['GET', 'POST'])
def qyweixin_authorization():
    global wxcpt
    import xml.etree.cElementTree as ET
    arg = request.args
    sVerifyMsgSig = arg['msg_signature']
    sVerifyTimeStamp = arg['timestamp']
    sVerifyNonce = arg['nonce']
    if not wxcpt or not isinstance(wxcpt, WXBizMsgCrypt):
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
        print('sMsg', sMsg)
        msg_type = xml_tree.find("MsgType").text
        from_user = xml_tree.find('ToUserName').text
        to_user = xml_tree.find('FromUserName').text
        if 'text' in msg_type:
            content = xml_tree.find("Content").text
            print(content)
            if content.startswith("http") and wxcpt.verify_url == can_commit:
                wxcpt.verify_url = content
                wxcpt.verify_operation = can_commit
                res_content = "please input operation"
            elif wxcpt.verify_operation == can_commit:
                wxcpt.verify_operation = content
                res_content = "waiting..."
                print(wxcpt.verify_url, wxcpt.verify_operation)
                verifycode_handle.apply_async(kwargs={'url': wxcpt.verify_url, 'operation': wxcpt.verify_operation})
                wxcpt.verify_code = can_commit
                wxcpt.verify_url = None
                wxcpt.verify_operation = None
            elif wxcpt.verify_code == can_commit:
                r = redis.Redis(host='localhost', port=6379, db=0)
                r.set('code', content, ex=10)
                res_content = "success to input code"
                wxcpt.verify_code = None
            elif content == "stop":
                wxcpt.weibo = None
                wxcpt.classify_tag = False
                wxcpt.classify = False
                res_content = "ok"
            elif wxcpt.classify_tag and int(content):
                wxcpt.weibo.add_tags(tag_ids=int(content))
                weibo = get_classify_weibo(mode=2)
                wxcpt.weibo = weibo
                res_content = ""
                tag_msg = get_tags_msg()
                msg = "正文: {}\n标签: {}".format(weibo.content, tag_msg)
                send_chinese_msg(msg)
            elif wxcpt.post_tag == True:
                import re
                re_post = re.match("type:(.*?);name:(.*?);", content)
                if re_post:
                    from web.models import Tag
                    type = re_post.group(1)
                    name = re_post.group(2)
                    if type not in Tag.type_set:
                        res_content = "tag type wrong,({})".format(Tag.type_set)
                    else:
                        tag = Tag()
                        tag.name = name
                        tag.type = type
                        db.session.add(tag)
                        db.session.commit()
                        res_content = "success".format(name)
                        wxcpt.post_tag = False
                else:
                    res_content = "format wrong"
            else:
                res_content = "我根本唔知你讲紧乜"

        elif 'event' in msg_type:
            event_key = xml_tree.find("EventKey").text
            print(event_key)
            if event_key == 'verifycode':
                res_content = "please input url"
                wxcpt.verify_url = can_commit
                wxcpt.verify_operation = can_commit
            elif event_key == 'crawl_weixin':
                crawl.apply_async(kwargs={'operation': 'weixin'})
                res_content = "crawling..."
            elif event_key == 'crawl_weibo':
                crawl.apply_async(kwargs={'operation': 'weibo'})
                res_content = "crawling..."
            elif event_key.startswith("classify"):
                file_path = config.PROJECT_PATH + "/weibo_nlp/"
                if wxcpt.classify and event_key == "classify_else":
                    print(wxcpt.weibo.content)
                    # write_weibo(file_path + 'else.txt', wxcpt.weibo.content)
                    save_classify_weibo_mode(wxcpt.weibo, '2')
                    weibo = get_classify_weibo()
                    wxcpt.weibo = weibo
                    res_content = ""
                    msg = "下一个: {}".format(weibo.content)
                    send_chinese_msg(msg)
                elif wxcpt.classify and event_key == "classify_pos":
                    print(wxcpt.weibo.content)
                    # write_weibo(file_path + 'pos.txt', wxcpt.weibo.content)
                    save_classify_weibo_mode(wxcpt.weibo, '0')
                    weibo = get_classify_weibo()
                    wxcpt.weibo = weibo
                    res_content = ""
                    msg = "下一个: {}".format(weibo.content)
                    send_chinese_msg(msg)
                elif wxcpt.classify and event_key == "classify_neg":
                    print(wxcpt.weibo.content)
                    # write_weibo(file_path + 'neg.txt', wxcpt.weibo.content)
                    save_classify_weibo_mode(wxcpt.weibo, '1')
                    weibo = get_classify_weibo()
                    wxcpt.weibo = weibo
                    res_content = ""
                    msg = "下一个: {}".format(weibo.content)
                    send_chinese_msg(msg)
                elif event_key == "classify_weibo":
                    weibo = get_classify_weibo()
                    wxcpt.weibo = weibo
                    wxcpt.classify = True
                    res_content = ""
                    msg = "开始: {}".format(weibo.content)
                    send_chinese_msg(msg)
                elif event_key == "classify_tag":
                    wxcpt.classify_tag = True
                    weibo = get_classify_weibo(mode=2)
                    wxcpt.weibo = weibo
                    res_content = ""
                    tag_msg = get_tags_msg()
                    msg = "正文: {}\n标签: {}".format(weibo.content, tag_msg)
                    send_chinese_msg(msg)
                else:
                    res_content = "error"
            elif event_key == "post_tag":
                wxcpt.post_tag = True
                res_content = "please input tag info like'type:{type};name:{name}'"
            else:
                res_content = "without this event"
        else:
            res_content = "I don't know what you say,please input again"
        res = api_tool.msg_encrp(wxcpt=wxcpt, to_user=to_user, from_user=from_user, content=res_content,
                                 sReqNonce=sVerifyNonce)
        response = make_response(res)
        response.content_type = 'application/xml'
        return response


def get_tags_msg():
    from web.models import Tag
    tags = Tag.query.filter_by(type='function').all()
    msg = ""
    for tag in tags:
        msg = msg + "{}-{};".format(tag.name, tag.tag_id)
    return msg


def send_chinese_msg(msg):
    from qyweixin.qyweixin_api import send_weixin_message, qyweixin_text_type
    send_weixin_message(send_type=qyweixin_text_type, msg_content=msg)


def save_classify_weibo_mode(weibo, mode):
    weibo.mode = mode
    db.session.add(weibo)
    db.session.commit()


def get_classify_weibo(mode=None):
    from web.models import Weibo
    weibo = Weibo.query.filter_by(mode=mode).order_by(Weibo.publish_time.desc()).first()
    return weibo


def write_weibo(file_path, str):
    f = open(file_path, 'w+')
    f.write(str)
    f.write('\n\n')
    f.close()


@main_blueprint.route('/api/reason', methods=['GET'])
def get_delete_reason():
    from web.models import Weibo_to_delete
    reason_dict = Weibo_to_delete.reason_choices_dict
    res = []
    for k, v in reason_dict.items():
        res.append({'id': k, 'content': v})
    return jsonify(res)


@main_blueprint.route('/api/tags', methods=['GET'])
def get_weibo_tags():
    from web.models import Tag
    ms = Tag.query.all()
    return jsonify(Tag.to_list(ms))

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
