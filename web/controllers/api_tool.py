from flask import current_app
from web import config, models
import requests
import json


def msg_encrp(wxcpt, to_user, from_user, content, sReqNonce):
    import time
    timestamp = str(int(time.time()))
    sRespData = """
            <xml>
            <ToUserName><![CDATA[{to_user}]]></ToUserName>
            <FromUserName><![CDATA[{from_user}]]></FromUserName>
            <CreateTime>{timestamp}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{content}]]></Content>
            </xml>
        """.format(to_user=to_user, from_user=from_user, timestamp=timestamp, content=content)
    print('sRespData', sRespData)
    ret, sEncryptMsg, item = wxcpt.EncryptMsg(sRespData, sReqNonce, timestamp)
    if (ret != 0):
        raise ValueError("ERR: EncryptMsg ret: " + str(ret))
    return sEncryptMsg


def do_requests(url, method, data=None, params=None, headers=None):
    if not headers:
        headers = {"content-type": "application/json"}
    try:
        res = requests.request(method=method, url=url, params=params, headers=headers, json=data)
        print(method, res.url, params, data)
        return True, res
    except Exception as e:
        print('请求失败', method, url, params, data, e)
        return False, str(e)


def weixin_authorization(username, js_code):
    base_url = config.WEIXIN_AUTH_URL
    url = base_url.format(JSCODE=js_code)
    flag, res = do_requests(url=url, method='get')
    if not flag:
        return flag, res
    if res.status_code == 200:
        res_json = res.json()
        if 'session_key' in res_json:
            openid = res_json['openid']
            session_key = res_json['session_key']
            expires_in = res_json['expires_in']
            value = {'openid': openid, 'session_key': session_key, 'expires_in': expires_in}
            third_session = models.User.gen_3rdsession(value=value).decode('utf-8')
            print(username, third_session, expires_in)
            meta = {'openid': openid, 'session_key': session_key,
                    'expires_in': expires_in, 'third_session': third_session}
            return True, {'third_session': third_session}, meta
        elif 'errcode' in res_json:
            return False, res_json['errmsg']
    return False, 'request error'
