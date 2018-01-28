from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


def gen_3rdsession(value):
    # 用OpenId加密生成3rdsession
    s = Serializer(current_app.config['SECRET_KEY'])
    third_session = s.dumps(value)
    return third_session


def gen_openId(thirdsession):
    # 用3rdsession解密生成OpenId
    s = Serializer(current_app.config['SECRET_KEY'])
    res = s.loads(thirdsession)
    return res


def msg_encrp(wxcpt, to_user, content, sReqNonce):
    import time
    timestamp = str(int(time.time()))
    sRespData = """
            <xml>
           <ToUserName><![CDATA[{to_user}]]></ToUserName>
           <FromUserName><![CDATA[{to_user}]]></FromUserName>
           <CreateTime>{timestamp}</CreateTime>
           <MsgType><![CDATA[text]]></MsgType>
           <Content><![CDATA[{content}]]></Content>
           </xml>
        """.format(to_user=to_user, timestamp=timestamp, content=content.encode('utf-8'))
    ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, sReqNonce, timestamp)
    if (ret != 0):
        raise ValueError("ERR: EncryptMsg ret: " + str(ret))
    return sEncryptMsg