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