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
            <ToUserName>{to_user}</ToUserName>
            <FromUserName>{from_user}</FromUserName>
            <CreateTime>{timestamp}</CreateTime>
            <MsgType>text</MsgType>
            <Content>{content}</Content>
            </xml>
        """.format(to_user=to_user, from_user=from_user, timestamp=timestamp, content=content)
    print(sRespData)
    ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, sReqNonce, timestamp)
    if (ret != 0):
        raise ValueError("ERR: EncryptMsg ret: " + str(ret))
    return sEncryptMsg


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


def get_code():
    code = input('输入验证码')
    return code


if __name__ == '__main__':
    print(timeoutFn(get_code, timeout_duration=5, default='no'))
