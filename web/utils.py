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
    ret, sEncryptMsg,item = wxcpt.EncryptMsg(sRespData, sReqNonce, timestamp)
    if (ret != 0):
        raise ValueError("ERR: EncryptMsg ret: " + str(ret))
    res = """
    <xml>
<Encrypt><![CDATA[m69NhQ1UCXVSV4nbqh0o/8Dw/+7uHQuabEFLpb5Sss8SYne1C/F/JUwECLZ3+6BEQcFYowh+PXGjOCRRm0REYLs9461btuOl/NUoqCUNpS9lcKp+VJANiM+wn2ULFjJGYw8w1VPs9OPuaPzGy53tY1iERy//eSV3o2y3H6f9W/JEdD8BF66g1uOKq7V15OwRNCVsNUKLWnbq8+UxigZqCqPXlPjXr7ZqbygfhopkADjJN2ijc1EzEuQ9FBHOORP+UPgch/BNp5Edf4W/m81aqEiifoabjOq/ChfniaahawstaJNaWJ3cCKnI+uP4xw7bDUegVI26FKI1TFrv4WRp3ISBr2u03AZj+/g9rzG7e2c0+cUZSpwKRu6epGQoERxwY3avuMvrgVsMZ3X8zGw7B7DQLt/o0ImpEP20Shx/swxOi6+roOP1fPq0yNr+ccPXEUSXb9TxxVBizCGhkPHz5w==]]></Encrypt>
<MsgSignature><![CDATA[4b07f10c27d4537e159a88d90cbda858b4513f5b]]></MsgSignature>
<TimeStamp>1517375802</TimeStamp>
<Nonce><![CDATA[1597212914]]></Nonce>
</xml>
    """
    return res


def timeoutFn(func, kwargs={}, timeout_duration=1, default=None):
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        print('time out')
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(**kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    return result
