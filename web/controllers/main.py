from flask import (current_app,
                   Blueprint,
                   request,
                   jsonify,
                   make_response,
                   render_template,
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
    template_folder='../templates',
)

can_commit = 'can_commit'
wxcpt = None


@main_blueprint.route('/api/handsome')
def index():
    return """
    城哥最帅
    城哥真的真的很帅"""


@main_blueprint.route('/api/report')
def report():
    from web.models import Report_detail
    arg = request.args
    year = arg.get('year', None)
    month = arg.get('month', None)
    report_id = "{}_{}".format(year, month)
    report = Report_detail.get(id=report_id, ignore=False)
    report_dict = Report_detail.to_dict(report)
    return render_template('report.html', report=report_dict)


@main_blueprint.route('/api/test')
def test():
    from weibo_nlp.word_cloud import get_word_cloud
    from weibo_nlp.weibo_count import zs_dxc_count, daily_weibo_count, recently_weibo_count
    from weibo_nlp.key_word import get_key_word
    from sqlalchemy import extract, and_
    from web.models import Report_detail, Weibo
    from elasticsearch_tool.init_models import Weixin
    from web.utils import str_md5
    from elasticsearch.exceptions import NotFoundError
    import datetime
    arg = request.args
    report_year = arg.get('year', None)
    report_month = arg.get('month', None)
    today = datetime.date.today()
    if not report_month:
        report_month = today.month
    if not report_year:
        report_year = today.year

    weibo_list = Weibo.query.filter(and_(
        extract('year', Weibo.publish_time) == report_year,
        extract('month', Weibo.publish_time) == report_month))
    content_list = [o.content for o in weibo_list.all()]
    file_name = get_word_cloud(content_list, report_year, report_month)
    zs_dxc_count(weibo_query=weibo_list)
    daily_weibo_count(weibo_query=weibo_list)
    recently_weibo_count(6, int(report_year), int(report_month))
    key_word_list = get_key_word(weibo_list)
    weibo_count = weibo_list.count()
    report_id = "{}_{}".format(report_year, report_month)
    report_res = Report_detail.get(report_id)
    report_res.month = report_month
    report_res.year = report_year
    report_res.count = weibo_count
    report_res.key_word = ", ".join(key_word_list)
    db.session.add(report_res)
    weixin_id = str_md5("{}_{}".format(report_year, report_month))
    try:
        weixin = Weixin.get(weixin_id)
    except NotFoundError:
        weixin = Weixin()
        weixin._id = weixin_id
    weixin.title = "{}年{}月树洞总结!!!".format(report_year, report_month)
    weixin.content = " "
    weixin.digest = '月度总结,先睹为快~~'
    weixin.publish_time = datetime.datetime.strptime(str(datetime.date(year=int(report_year), month=int(report_month), day=1)),
                                                     "%Y-%m-%d")
    weixin.cover = "https://www.akcia.cn/static/{}".format(file_name)
    weixin.url = "https://www.akcia.cn/api/report?year={}&month={}".format(report_year, report_month)
    weixin.gzh = "本平台"
    weixin.save()
    db.session.commit()
    print('完成{}月总结'.format(report_month))
    return 'end'


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


@main_blueprint.route('/api/article', methods=['GET'])
def get_weixin_article():
    arg = request.args
    article_id = arg.get('articleId', '')
    if not article_id:
        return jsonify(404)
    return render_template('{}.html'.format(article_id))


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
